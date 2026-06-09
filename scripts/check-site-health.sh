#!/bin/sh
set -eu

check_url() {
  url="$1"
  status="$(curl \
    --silent \
    --show-error \
    --location \
    --retry 2 \
    --retry-all-errors \
    --connect-timeout 10 \
    --max-time 30 \
    --output /dev/null \
    --write-out '%{http_code}' \
    "$url")"

  if [ "$status" != "200" ]; then
    echo "Health check failed for $url: HTTP $status" >&2
    return 1
  fi

  echo "OK $status $url"
}

check_url "https://softmoonstudio.com/"
check_url "https://softmoonstudio.com/posts/best-essential-oil-diffusers-that-look-like-home-decor/"
