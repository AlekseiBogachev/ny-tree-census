#!/bin/bash
docker build \
--tag self-hosted-runner \
--progress=plain \
--no-cache \
--file ./gh_actions_runner/Dockerfile \
. \
2>&1 | tee ./logs/docker_build.log