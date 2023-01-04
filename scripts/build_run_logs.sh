#!/bin/bash
scripts/build-docker.sh
docker kill fmmel
scripts/run.sh
docker logs -f fmmel
