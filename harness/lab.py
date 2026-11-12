"""Run with `uv run python -m harness.lab --help`. Never starts the trading app."""

import argparse
import hashlib
import importlib.metadata
import json
import os
import platform
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "upstream.json"
REPORTS = ROOT / "quality-lab/reports/generated"


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def manifest() -> dict:
    return json.loads(MANIFEST.read_text())


def source_path() -> Path:
    return ROOT / manifest()["checkout"]


def verify_source() -> dict:
    pin = manifest()
    source = source_path()
    if not (source / ".git").exists():
        raise RuntimeError("OpenAlgo is missing. Run: uv run python -m harness.lab bootstrap")
    actual = git("rev-parse", "HEAD", cwd=source)
    if actual != pin["commit"]:
        raise RuntimeError(f"Wrong upstream revision: {actual}; expected {pin['commit']}")
    for relative, expected in pin["component_sha256"].items():
        actual_hash = hashlib.sha256((source / relative).read_bytes()).hexdigest()
        if actual_hash != expected:
            raise RuntimeError(f"Upstream component changed: {relative}; restore before testing.")
    return pin


def bootstrap() -> None:
    pin = manifest()
    source = source_path()
    if source.exists():
        verify_source()
        print("Existing OpenAlgo checkout matches the pin; left unchanged.")
        return
    # Stage first so an interrupted fetch cannot leave a half-prepared source directory.
    with tempfile.TemporaryDirectory(prefix="openalgo-bootstrap-", dir=ROOT) as directory:
        staged = Path(directory) / "source"
        staged.mkdir()
        git("init", cwd=staged)
        git("remote", "add", "origin", pin["repository"], cwd=staged)
        git("fetch", "--depth=1", "origin", pin["commit"], cwd=staged)
        git("checkout", "--detach", "FETCH_HEAD", cwd=staged)
        staged.rename(source)
    verify_source()
    print(f"Prepared OpenAlgo at {pin['commit']}")


def evidence() -> dict:
    pin = verify_source()
    return {
        "lab_commit": git("rev-parse", "HEAD"),
        "lab_worktree_dirty": bool(git("status", "--porcelain")),
        "upstream_repository": pin["repository"],
        "upstream_commit": pin["commit"],
        "component_sha256": pin["component_sha256"],
        "python": platform.python_version(),
        "platform": platform.platform(),
        "dependencies": {
            name: importlib.metadata.version(name) for name in ("pytest", "marshmallow")
        },
        "profile": "schema-component; no HTTP, database, broker or model",
        "data": "synthetic NSE LIMIT order; explicit examples, no random generation",
        "seed": None,
        "retries": 0,
    }


def run_suite(label: str, schema_path: Path) -> tuple[int, list]:
    REPORTS.mkdir(parents=True, exist_ok=True)
    xml_path = REPORTS / f"{label}.xml"
    xml_path.unlink(missing_ok=True)
    env = os.environ.copy()
    env["LAB_UPSTREAM_PATH"] = str(source_path())
    env["LAB_SCHEMA_PATH"] = str(schema_path)
    # Keep inherited Python search paths from changing which code is measured.
    env.pop("PYTHONPATH", None)
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "quality-lab/tests", f"--junitxml={xml_path}"],
        cwd=ROOT,
        env=env,
        check=False,
        timeout=120,
    )
    if not xml_path.exists():
        raise RuntimeError(f"{label}: no JUnit evidence (pytest exit {result.returncode})")
    cases = list(ET.parse(xml_path).getroot().iter("testcase"))
    if not cases or any(case.find("skipped") is not None for case in cases):
        raise RuntimeError(f"{label}: zero cases or unexpected skips; this is not a passing run")
    if any(case.find("error") is not None for case in cases):
        raise RuntimeError(f"{label}: test setup/collection error; this is not mutation detection")
    return result.returncode, cases


def test() -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "baseline.json").unlink(missing_ok=True)
    details = evidence()
    code, cases = run_suite("baseline", source_path() / "restx_api/schemas.py")
    details.update(
        status="passed" if code == 0 else "failed",
        cases=len(cases),
        failures=sum(case.find("failure") is not None for case in cases),
        skips=0,
    )
    (REPORTS / "baseline.json").write_text(json.dumps(details, indent=2) + "\n")
    if code:
        raise RuntimeError(f"Baseline failed (pytest exit {code}); inspect baseline.xml")


def prove() -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "mutation-proof.json").unlink(missing_ok=True)
    # A failed baseline cannot be mistaken for a killed mutant.
    test()
    details = evidence()
    text = (source_path() / "restx_api/schemas.py").read_text()
    needle = "min_inclusive=False"
    start = text.index("class OrderSchema(")
    end = text.index("class SmartOrderSchema(")
    original = text[start:end]
    if original.count(needle) != 1:
        raise RuntimeError("Mutation target changed; review the pin and proof before proceeding")
    mutated = text[:start] + original.replace(needle, "min_inclusive=True") + text[end:]
    with tempfile.TemporaryDirectory(prefix="quality-lab-mutant-") as directory:
        schema = Path(directory) / "schemas.py"
        schema.write_text(mutated)
        code, cases = run_suite("mutant", schema)
    failures = [case for case in cases if case.find("failure") is not None]
    expected = "test_limit_order_quantity_boundary[zero-rejected]"
    if code != 1 or len(failures) != 1 or failures[0].get("name") != expected:
        raise RuntimeError("Mutant did not fail only the expected zero-quantity assertion")
    details.update(
        status="killed",
        mutation="OrderSchema.quantity: min_inclusive=False -> True",
        mutant_sha256=hashlib.sha256(mutated.encode()).hexdigest(),
        detected_by=expected,
        mutant_pytest_exit=code,
        mutant_cases=len(cases),
        failures=len(failures),
        skips=0,
    )
    (REPORTS / "mutation-proof.json").write_text(json.dumps(details, indent=2) + "\n")
    verify_source()
    print("Mutation killed by the expected assertion; upstream source was left unchanged.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["bootstrap", "doctor", "test", "prove"])
    args = parser.parse_args()
    try:
        match args.command:
            case "bootstrap":
                bootstrap()
            case "doctor":
                print(json.dumps(evidence(), indent=2))
            case "test":
                test()
            case "prove":
                prove()
    except (RuntimeError, OSError, subprocess.SubprocessError, ValueError) as error:
        print(f"Lab error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
