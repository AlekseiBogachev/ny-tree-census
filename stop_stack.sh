#!/bin/bash

docker compose exec self-hosted_runner \
./config.sh remove --token \
$(docker compose exec self-hosted_runner cat /run/secrets/runner_secret_token)

docker compose down