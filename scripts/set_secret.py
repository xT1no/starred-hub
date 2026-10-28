#!/usr/bin/env python3
"""写入 GitHub Actions Secret（libsodium sealed box）。

用法：
    GH_TOKEN=xxx python scripts/set_secret.py <owner/repo> <SECRET_NAME> <SECRET_VALUE>
"""
import base64
import json
import os
import sys
import urllib.request


def api(method, url, token, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + token)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if data:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=30) as r:
        body = r.read()
        return r.status, (json.loads(body) if body.strip() else None)


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        return 1
    repo, name, value = sys.argv[1], sys.argv[2], sys.argv[3]
    token = os.environ.get("GH_TOKEN")
    if not token:
        print("缺少环境变量 GH_TOKEN")
        return 1

    from nacl import encoding, public

    _, key = api("GET", f"https://api.github.com/repos/{repo}/actions/secrets/public-key", token)
    pk = public.PublicKey(key["key"].encode(), encoding.Base64Encoder())
    sealed = public.SealedBox(pk).encrypt(value.encode())

    status, _ = api(
        "PUT",
        f"https://api.github.com/repos/{repo}/actions/secrets/{name}",
        token,
        {"encrypted_value": base64.b64encode(sealed).decode(), "key_id": key["key_id"]},
    )
    print(f"{name} -> HTTP {status} ({'已写入' if status in (201, 204) else '失败'})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
