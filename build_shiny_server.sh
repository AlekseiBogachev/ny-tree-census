#!/bin/bash

echo "" | tee -a ./logs/docker_build.log
echo "Сборка Shiny Server" | tee -a ./logs/docker_build.log
echo "" | tee -a ./logs/docker_build.log

BUILDKIT_PROGRESS=plain \
docker build \
--tag shiny_server \
--progress=plain \
--target shiny_server \
. \
2>&1 | tee -a ./logs/docker_build.log
