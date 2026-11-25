#!/usr/bin/env python3
"""Upload an AASX package or inspect shells using the BaSyx REST API."""
import argparse
import json
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from uuid import uuid4

MIME = "application/asset-administration-shell-package"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://localhost:8081")
    sub = parser.add_subparsers(dest="command", required=True)
    upload = sub.add_parser("upload")
    upload.add_argument("file", type=Path)
    sub.add_parser("list")
    args = parser.parse_args()
    base = args.url.rstrip("/")
    try:
        if args.command == "upload":
            boundary = uuid4().hex
            filename = args.file.name.replace('"', '_').replace('\r', '_').replace('\n', '_')
            body = (f'--{boundary}\r\nContent-Disposition: form-data; name="file"; '
                    f'filename="{filename}"\r\nContent-Type: {MIME}\r\n\r\n').encode()
            body += args.file.read_bytes() + f'\r\n--{boundary}--\r\n'.encode()
            request = Request(base + "/upload", data=body, headers={
                "Content-Type": f"multipart/form-data; boundary={boundary}", "Accept": "*/*"})
        else:
            request = Request(base + "/shells", headers={"Accept": "application/json"})
        with urlopen(request, timeout=60) as response:
            data = response.read().decode(errors="replace")
            print(f"HTTP {response.status}")
            if data:
                try:
                    print(json.dumps(json.loads(data), indent=2))
                except ValueError:
                    print(data)
    except HTTPError as error:
        parser.exit(1, f"HTTP {error.code}: {error.read().decode(errors='replace')}\n")
    except (URLError, OSError) as error:
        parser.exit(1, f"Request failed: {error}\n")


if __name__ == "__main__":
    main()
