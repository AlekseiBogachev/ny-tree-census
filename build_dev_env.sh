#!/bin/bash

echo "" | tee -a ./logs/docker_build.log
echo "Сборка базового образа и образа среды разработки" | tee -a ./logs/docker_build.log
echo "" | tee -a ./logs/docker_build.log

BUILDKIT_PROGRESS=plain \
docker build \
--tag ny_tree_census_dev \
--progress=plain \
--no-cache \
--secret id=pat,src=.dev_env_pat \
--target ny_tree_census_dev \
. \
2>&1 | tee -a ./logs/docker_build.log
