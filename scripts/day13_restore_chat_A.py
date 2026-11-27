"""Restore an actual local A+guard snapshot to the isolated Day 13 chat flow."""
import json
import os
from pathlib import Path
import sys
from datetime import datetime, timezone
from day13_publish_chat_marker import aws, TARGET, MARKER, MESSAGE


def main():
    os.umask(0o077)
    root = Path.home() / "Neptune-Day13-Backups"
    rollback = sorted(root.glob("rollback-*/A-flow-response.json"))
    context = sorted(root.glob("context-*/recovery-after.json"))
    choices = rollback or context
    if not choices:
        raise RuntimeError("No saved A + context snapshot found.")
    anchor = choices[-1]
    saved = json.loads(anchor.read_text())
    content = json.loads(saved["Content"])
    actions = {a["Identifier"]: a for a in content["Actions"]}
    if (saved["Name"] != TARGET or content["StartAction"] != MARKER
            or actions[MARKER]["Parameters"].get("Text") != MESSAGE
            or "Day13 Context Check" not in actions or "Day13 Missing Context" not in actions):
        raise RuntimeError("Snapshot is not the intended A + context baseline.")
    arn = saved["Arn"]
    iid = arn.split(":instance/", 1)[1].split("/")[0]
    fid = arn.split("/contact-flow/", 1)[1].split(":")[0]
    if aws("sts", "get-caller-identity")["Account"] != arn.split(":")[4]:
        raise RuntimeError("AWS account mismatch.")
    before = aws("connect", "describe-contact-flow", "--instance-id", iid,
                 "--contact-flow-id", fid)["ContactFlow"]
    if before["Name"] != TARGET:
        raise RuntimeError("Current flow name mismatch.")
    folder = root / ("restore-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ"))
    folder.mkdir(parents=True, exist_ok=False)
    (folder / "before.json").write_text(json.dumps(before, indent=2))
    path = folder / "restored-A-content.json"
    path.write_text(json.dumps(content, indent=2, ensure_ascii=False))
    aws("connect", "update-contact-flow-content", "--instance-id", iid,
        "--contact-flow-id", fid, "--content", "file://" + str(path))
    after = aws("connect", "describe-contact-flow", "--instance-id", iid,
                "--contact-flow-id", fid)["ContactFlow"]
    (folder / "after.json").write_text(json.dumps(after, indent=2))
    if after.get("Status") != "PUBLISHED" or json.loads(after["Content"])["Actions"] != content["Actions"]:
        raise RuntimeError("Restored published graph was not confirmed.")
    print("PASS: A + context baseline restored and confirmed by read-back.")
    print("Evidence saved:", folder)
    print("Verify a fresh customer chat before closing the incident.")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, KeyError, ValueError, OSError) as error:
        print("STOP:", error, file=sys.stderr)
        sys.exit(1)
