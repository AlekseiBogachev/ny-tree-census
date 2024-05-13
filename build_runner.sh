#!/bin/bash
echo "" | tee -a ./logs/docker_build.log
echo "Сборка образа GitHub Actions self-hosted runner" | tee -a ./logs/docker_build.log
echo "" | tee -a ./logs/docker_build.log

docker build \
--tag self-hosted_runner \
--progress=plain \
--no-cache \
--target gh_actions_runner \
. \
2>&1 | tee -a ./logs/docker_build.log
