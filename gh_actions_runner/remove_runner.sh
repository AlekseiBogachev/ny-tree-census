#!/bin/bash
docker exec -it ny_tree_census_runner ./config.sh \
remove --token $(cat ./gh_actions_runner/.secret_token)
# docker image rm -f self-hosted-runner
