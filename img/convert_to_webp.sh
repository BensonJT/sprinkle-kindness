#!/usr/bin/env bash
# One-time migration: img/*.{jpg,JPG,heic,HEIC} -> img/webp/*.webp
# - Detects real HEIF vs mislabeled JPEG-as-.heic by magic bytes.
# - Downscales long edge to 2000px (no upscaling).
# - Strips EXIF/GPS metadata.
set -euo pipefail

cd "$(dirname "$0")"
OUTDIR="webp"
QUALITY=82
MAXDIM=2000
SCALE_FILTER="scale='if(gt(iw,ih),min(${MAXDIM},iw),-2)':'if(gt(ih,iw),min(${MAXDIM},ih),-2)'"

mkdir -p "$OUTDIR"

shopt -s nullglob nocaseglob
files=(*.jpg *.heic)
shopt -u nocaseglob

count=0
for f in "${files[@]}"; do
  base="$(basename "${f%.*}")"
  out="$OUTDIR/${base}.webp"

  kind="$(file -b "$f")"
  if [[ "$kind" == *"ISO Media"*"HEIF"* ]]; then
    tmp="$(mktemp --suffix=.png)"
    heif-convert -q 100 "$f" "$tmp" >/dev/null 2>&1
    ffmpeg -y -loglevel error -i "$tmp" -map_metadata -1 \
      -vf "$SCALE_FILTER" -c:v libwebp -quality "$QUALITY" "$out"
    rm -f "$tmp" "${tmp%.png}-depth.png"
  else
    # Mislabeled or plain JPEG: force mjpeg demuxer, take only frame 1
    # (frame 2+ can be an embedded EXIF thumbnail).
    ffmpeg -y -loglevel error -f mjpeg -i "$f" -frames:v 1 -map_metadata -1 \
      -vf "$SCALE_FILTER" -c:v libwebp -quality "$QUALITY" "$out"
  fi

  count=$((count + 1))
  echo "[$count/${#files[@]}] $f -> $out"
done

echo "Done. Converted $count files into $OUTDIR/"
