#!/usr/bin/env python3
"""Verify a controlled timeout and restore Neptune Insurance lookup settings."""

import json
import subprocess
import sys
import tempfile
from pathlib import Path


FUNCTION = "NeptuneInsuranceLookup"
REGION = "us-west-2"
EXPECTED_ROLE = "arn:aws:iam::690405831841:role/NeptuneInsuranceLookupRole"
FIXTURE = Path(__file__).resolve().parents[1] / "events" / "claim-owned.json"


def aws(*arguments):
    completed = subprocess.run(
        ["aws", *arguments, "--region", REGION, "--output", "json", "--no-cli-pager"],
        capture_output=True,
        text=True,
    )
    if completed.returncode:
        raise RuntimeError(completed.stderr.strip() or "AWS CLI request failed")
    return json.loads(completed.stdout) if completed.stdout.strip() else None


def configuration():
    return aws("lambda", "get-function-configuration", "--function-name", FUNCTION)


def wait_updated():
    aws("lambda", "wait", "function-updated-v2", "--function-name", FUNCTION)


def configure(timeout, variables):
    current = configuration()
    if current.get("LastUpdateStatus") == "InProgress":
        wait_updated()
        current = configuration()
    aws(
        "lambda", "update-function-configuration",
        "--function-name", FUNCTION,
        "--revision-id", current["RevisionId"],
        "--timeout", str(timeout),
        "--environment", json.dumps({"Variables": variables}),
    )
    wait_updated()


def invoke(directory, label):
    output = directory / (label + ".json")
    metadata = aws(
        "lambda", "invoke",
        "--function-name", FUNCTION,
        "--invocation-type", "RequestResponse",
        "--payload", "fileb://" + str(FIXTURE),
        str(output),
    )
    return metadata, json.loads(output.read_text())


def main():
    original = configuration()
    variables = original.get("Environment", {}).get("Variables", {})
    if original.get("Role") != EXPECTED_ROLE:
        raise RuntimeError("Unexpected execution role/account; no settings changed")
    if original.get("State") != "Active":
        raise RuntimeError("Function must be Active before this check")
    if (
        original.get("Timeout") != 3
        or variables.get("LOOKUP_DELAY_SECONDS") != "0"
        or variables.get("DEMO_CUSTOMER_ID") != "DEMO-1001"
        or variables.get("TABLE_NAME") != "NeptuneInsuranceLab"
    ):
        raise RuntimeError("Function differs from the verified baseline; no settings changed")
    if not FIXTURE.is_file():
        raise RuntimeError("Missing claim-owned.json; pull the project first")

    fault_variables = dict(variables)
    fault_variables["LOOKUP_DELAY_SECONDS"] = "2"
    observed_timeout = False

    with tempfile.TemporaryDirectory(prefix="neptune-timeout-") as temporary:
        directory = Path(temporary)
        try:
            print("Temporarily setting timeout=1 second and delay=2 seconds.", flush=True)
            configure(1, fault_variables)
            metadata, response = invoke(directory, "timeout")
            description = json.dumps(response).lower()
            observed_timeout = (
                metadata.get("StatusCode") == 200
                and bool(metadata.get("FunctionError"))
                and ("timed out" in description or "timeout" in description)
            )
            print("Timeout response:", json.dumps(response), flush=True)
            if observed_timeout:
                print("PASS controlled timeout observed.", flush=True)
            else:
                print("FAIL expected a Lambda timeout error.", flush=True)
        finally:
            print("Restoring the original timeout and environment variables.", flush=True)
            configure(original["Timeout"], variables)
            restored = configuration()
            if (
                restored.get("Timeout") != original["Timeout"]
                or restored.get("Environment", {}).get("Variables", {}) != variables
                or restored.get("LastUpdateStatus") != "Successful"
            ):
                raise RuntimeError("Restoration could not be verified; inspect configuration")
            print("PASS settings restored: timeout=3, delay=0.", flush=True)

        metadata, response = invoke(directory, "recovery")
        if (
            metadata.get("StatusCode") != 200
            or metadata.get("FunctionError")
            or response.get("resultCode") != "OK"
            or response.get("reference") != "CLM-1001"
            or response.get("status") != "IN_REVIEW"
            or response.get("product") != "AUTO"
        ):
            raise RuntimeError("Recovery lookup failed: " + json.dumps(response))
        print("PASS recovery lookup: OK | requestId=" + response["requestId"], flush=True)

    if not observed_timeout:
        return 1
    print("Timeout and recovery passed. Next: Connect integration.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (RuntimeError, OSError, ValueError, KeyError, TypeError) as error:
        print("STOP: " + str(error), file=sys.stderr)
        print("Paste this output before continuing.", file=sys.stderr)
        sys.exit(1)
