#!/bin/sh
# Run with:
#     scripts/upload.sh
#####
# You need to be logged in to the registry to upload.

docker build -t fmonera/fmmel:latest .
docker push fmonera/fmmel:latest

