#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ -f "$root_dir/.env" ]]; then
  echo "Exists: $root_dir/.env"
  exit 0
fi

if [[ ! -f "$root_dir/.env.example" ]]; then
  echo "Missing $root_dir/.env.example"
  exit 1
fi

cp "$root_dir/.env.example" "$root_dir/.env"
echo "Created: $root_dir/.env"
