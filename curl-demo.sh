#!/usr/bin/env bash
set -e

API="http://127.0.0.1:8000/api/v1"

curl -X POST "$API/assets/register" \
  -F "title=Official Match Poster" \
  -F "asset_type=image" \
  -F "owner=RCB Media Team" \
  -F "league=IPL" \
  -F "visible_watermark=true" \
  -F "file=@./sample_data/official_poster.jpg"

curl -X POST "$API/scans/upload-evidence" \
  -F "source_label=pirate-instagram-repost" \
  -F "platform=instagram" \
  -F "file=@./sample_data/suspicious_poster.jpg"
