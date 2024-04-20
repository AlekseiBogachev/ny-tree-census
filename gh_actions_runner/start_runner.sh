#!/bin/bash
docker run \
--rm \
-it \
--name ny_tree_census_runner \
self-hosted-runner /bin/bash -c "\
./config.sh \
--replace \
--unattended \
--name ubuntu-ds-runner \
--labels ubuntu,ds,no-gpu \
--url https://github.com/AlekseiBogachev/ny-tree-census \
--token $(cat ./gh_actions_runner/.secret_token) && \
./run.sh"