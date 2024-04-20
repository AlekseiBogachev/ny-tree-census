#!/bin/bash

echo "Сборка базового образа" | tee ./logs/docker_build.log

docker build \
--build-arg GITUSER="$(git config user.name)" \
--build-arg GITEMAIL="$(git config user.email)" \
--build-arg REPO="AlekseiBogachev/ny-tree-census.git" \
-t ny_tree_census_base \
--progress=plain \
. \
2>&1 | tee -a ./logs/docker_build.log

echo "Сборка образа среды разработки" | tee ./logs/docker_build.log

BUILDKIT_PROGRESS=plain \
docker build \
-f Dockerfile_dev_env \
-t ny_tree_census_dev \
--progress=plain \
--no-cache \
--secret id=pat,src=.dev_env_pat \
. \
2>&1 | tee -a ./logs/docker_build.log
