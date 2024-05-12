#!/bin/bash
docker exec -it ny_tree_census_runner ./config.sh \
remove --token $(cat .runner_secret_token)
