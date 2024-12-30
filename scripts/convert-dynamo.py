#!/usr/bin/env python3

import json
from pathlib import Path


def convert(fp: Path):
    dat: dict = json.loads(fp.read_text())
    rm = f"""# {dat['name']}

{dat['desc']}
"""
    
    for label, value in [
        ("Workflow Engine", dat.get("executor").title()),
        ("Category", dat.get("category")),
        ("Documentation", (
            None if dat.get("documentationUrl") is None
            else f"[{dat['documentationUrl']}]({dat['documentationUrl']})"
        )),
        ("Source", f"[{dat['code']['uri']}]({dat['code']['uri']})"),
        ("Version", f"`{dat['code']['version']}`"),
        ("Script", f"`{dat['code']['script']}`"),
    ]:
        rm += f"""

{label}: {value}
"""

    with open(fp.parent / "README.md", "w") as f:
        f.write(rm)
    fp.unlink()


def main():

    for file in Path("workflows").rglob("process-dynamo.json"):
        convert(file)


if __name__ == "__main__":
    main()