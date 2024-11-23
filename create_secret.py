#!/usr/bin/env python3
import os
import re
import sys
import tempfile
from typing import Optional

DEFAULT_SCOPE = "api.bsky.app"


def usage():
    print("Usage: set_bearer_token.py <bearer_token> [<scope>]")


def valid_token(token: str) -> bool:
    return re.match(r"^[a-zA-Z0-9\._\-]+$", token) is not None


def get_secret_name(scope: str) -> str:
    scope = re.sub(r"^.+?://", "", scope)
    scope = re.sub(r"[^a-zA-Z0-9]", "_", scope)
    return f"atproto_{scope}"


def get_secret_sql(token: str, scope: Optional[str] = None) -> str:
    lines = []
    scope = scope or DEFAULT_SCOPE
    secret_name = get_secret_name(scope)

    lines.append(f"DROP SECRET IF EXISTS {secret_name};")
    authorization_header = f"Bearer {token}"
    extra_http_headers = {
        "Authorization": authorization_header,
    }
    extra_http_headers_map = repr(extra_http_headers)

    if "://" not in scope:
        scope = f"https://{scope}"
    scope_sql = f", SCOPE {repr(scope)}"
    lines.append(
        f"CREATE PERSISTENT SECRET {secret_name} ("
        f"TYPE HTTP, "
        f"EXTRA_HTTP_HEADERS MAP {extra_http_headers_map}"
        f"{scope_sql}"
        f");"
    )
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)
    token = sys.argv[1]
    if not valid_token(token):
        print("Invalid token")
        sys.exit(1)

    scope = sys.argv[2] if len(sys.argv) > 2 else None

    setup_sql = get_secret_sql(token=token, scope=scope)
    print(setup_sql)

    # write to temp file
    _, tmp_path = tempfile.mkstemp()
    with open(tmp_path, "w") as f:
        f.write(setup_sql)

    print(f"Creating duckdb secret {get_secret_name(scope)}")
    os.system(f"duckdb < {tmp_path}")
    os.unlink(tmp_path)


if __name__ == "__main__":
    main()
