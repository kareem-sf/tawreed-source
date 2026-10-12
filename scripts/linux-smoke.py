"""Clean-install smoke test for the Linux deb, run on a fresh Ubuntu 24.04 x86_64 machine after `apt install`.

Headless only: it starts the installed service with an isolated data folder and a synthetic BOQ, and writes
evidence files. It does not open the window and does not replace human Desktop acceptance (docs/release-runbook.md).

    python3 scripts/linux-smoke.py --deb PATH --fixture PDF --out DIR
"""

import argparse
import hashlib
import json
import os
import secrets
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path


def run(*command: str) -> str:
    return subprocess.run(command, check=True, capture_output=True, text=True).stdout


def free_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return probe.getsockname()[1]


def call(port: int, path: str, token: str | None = None, body: bytes | None = None, content_type: str | None = None):
    request = urllib.request.Request(f"http://127.0.0.1:{port}{path}", data=body, method="POST" if body else "GET")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    if content_type:
        request.add_header("Content-Type", content_type)
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return response.status, json.loads(response.read() or b"null")
    except urllib.error.HTTPError as error:
        return error.code, None


def multipart(name: str, filename: str, data: bytes) -> tuple[bytes, str]:
    boundary = uuid.uuid4().hex
    head = f'--{boundary}\r\nContent-Disposition: form-data; name="files"; filename="{filename}"\r\n'
    head += "Content-Type: application/pdf\r\n\r\n"
    body = head.encode() + data + f"\r\n--{boundary}\r\nContent-Disposition: form-data; name=\"name\"\r\n\r\n{name}\r\n--{boundary}--\r\n".encode()
    return body, f"multipart/form-data; boundary={boundary}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--deb", type=Path, required=True)
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    checks: list[dict] = []

    def check(name: str, ok: bool, detail: str = "") -> None:
        checks.append({"check": name, "ok": bool(ok), "detail": detail})
        print(("PASS " if ok else "FAIL ") + name + (f": {detail}" if detail else ""))

    os_release = Path("/etc/os-release").read_text()
    machine = os.uname().machine
    check("Ubuntu 24.04", 'VERSION_ID="24.04"' in os_release and "ID=ubuntu" in os_release)
    check("x86_64", machine == "x86_64", machine)

    deb_version = run("dpkg-deb", "--field", str(args.deb), "Version").strip()
    package = run("dpkg-deb", "--field", str(args.deb), "Package").strip()
    installed = run("dpkg-query", "-W", "-f=${Status} ${Version}", package).strip()
    check("package installed at the deb version", installed == f"install ok installed {deb_version}", installed)
    files = run("dpkg", "-L", package).splitlines()
    (args.out / "package-files.txt").write_text("\n".join(files) + "\n")
    service = next((Path(f) for f in files if f.endswith("/tawreed-service") and Path(f).is_file()), None)
    check("service binary installed", service is not None, str(service))
    desktop = next((Path(f) for f in files if f.startswith("/usr/bin/") and Path(f).is_file()), None)
    check("desktop binary installed", desktop is not None, str(desktop))
    if desktop:
        missing = [line.strip() for line in run("ldd", str(desktop)).splitlines() if "not found" in line]
        check("desktop binary has no missing libraries", not missing, "; ".join(missing))
    if service is None:
        (args.out / "evidence.json").write_text(json.dumps({"checks": checks}, indent=2))
        return 1

    home = Path(tempfile.mkdtemp(prefix="tawreed-smoke-"))
    data = home / "data"
    token, port = secrets.token_hex(16), free_port()
    log = (args.out / "service.log").open("w")
    # An empty environment: nothing from the runner leaks in, and the real ~/.tawreed is never touched.
    env = {"HOME": str(home), "TAWREED_HOME": str(data), "TAWREED_TOKEN": token, "PATH": "/usr/bin:/bin"}
    process = subprocess.Popen(
        [str(service), "--port", str(port), "--exit-with-stdin"], env=env, stdin=subprocess.PIPE, stdout=log, stderr=log
    )
    try:
        healthy = False
        for _ in range(60):
            try:
                healthy = call(port, "/health") == (200, {"status": "ok"})
            except OSError:
                pass
            if healthy or process.poll() is not None:
                break
            time.sleep(1)
        check("service answers /health", healthy)
        if healthy:
            check("a request without the token is refused", call(port, "/projects")[0] == 401)
            status, about = call(port, "/about", token)
            check("/about reports the deb version", status == 200 and about.get("version") == deb_version, str(about))
            check("data folder is the isolated one", about and about.get("data_folder") == str(data), str(about))
            body, content_type = multipart("Smoke test project", args.fixture.name, args.fixture.read_bytes())
            status, project = call(port, "/projects", token, body, content_type)
            check("synthetic BOQ starts a project", status == 201 and len(project["sources"]) == 1, f"HTTP {status}")
            status, listing = call(port, "/projects", token)
            check("project is listed", status == 200 and [p["name"] for p in listing] == ["Smoke test project"])
        check("state written only to the isolated folder", data.is_dir() and not (Path.home() / ".tawreed").exists())
    finally:
        # The desktop app keeps this pipe open; closing it must stop the service.
        process.stdin.close()
        try:
            exited = process.wait(timeout=10) == 0
        except subprocess.TimeoutExpired:
            process.kill()
            exited = False
        log.close()
        check("service exits when its parent closes stdin", exited)

    evidence = {
        "os": os_release.splitlines()[:4],
        "machine": machine,
        "deb": {"name": args.deb.name, "version": deb_version, "sha256": hashlib.sha256(args.deb.read_bytes()).hexdigest()},
        "fixture": args.fixture.name,
        "checks": checks,
        "scope": "Headless install and service check only. Human Desktop acceptance (window, Arabic rendering) is separate.",
    }
    (args.out / "evidence.json").write_text(json.dumps(evidence, indent=2) + "\n")
    return 0 if all(c["ok"] for c in checks) else 1


if __name__ == "__main__":
    sys.exit(main())
