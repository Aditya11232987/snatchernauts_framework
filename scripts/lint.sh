#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${RENPY_SDK:-}" ]]; then
  echo "RENPY_SDK is not set. Please export RENPY_SDK to your Ren'Py 8.4.x SDK path." >&2
  exit 1
fi

"$RENPY_SDK/renpy.sh" . lint
