#!/bin/bash

echo "" | tee -a ./logs/docker_build.log
echo "Сборка базового образа и устрановка в него пакетов Python" | tee \
-a ./logs/docker_build.log
echo "" | tee -a ./logs/docker_build.log

BUILDKIT_PROGRESS=plain \
docker build \
--tag ny_tree_census_packages \
--progress=plain \
--target ny_tree_census_packages \
. \
2>&1 | tee -a ./logs/docker_build.log
