#!/bin/sh
# Run with:
#     scripts/upload.sh
#####
# You need to be logged in to the registry to upload.

docker build -t ghcr.io/fmonera/fmmel:latest .
docker push ghcr.io/fmonera/fmmel:latest

