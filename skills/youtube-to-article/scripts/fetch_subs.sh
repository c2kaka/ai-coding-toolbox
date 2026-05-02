#!/usr/bin/env bash
set -euo pipefail

URL="${1:?Usage: fetch_subs.sh <youtube-url> [output-dir]}"
OUT_DIR="${2:-./youtube-to-artifact}"

mkdir -p "${OUT_DIR}"

yt-dlp --dump-json --skip-download "${URL}" > "${OUT_DIR}/metadata.json"

yt-dlp \
  --write-subs \
  --write-auto-subs \
  --sub-langs "en,zh-Hans,zh-Hant" \
  --skip-download \
  --sub-format vtt \
  -o "${OUT_DIR}/%(id)s" \
  "${URL}"

echo "Done. Metadata: ${OUT_DIR}/metadata.json"
echo "Subtitle files:"
ls -1 "${OUT_DIR}"/*.vtt 2>/dev/null || echo "(no .vtt found — video may lack captions)"
