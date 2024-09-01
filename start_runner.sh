#!/bin/bash

echo ""
echo "Создание контейнера и запуск GitHub Actions self-hosted runner"
echo ""

docker run \
--rm \
--detach \
--name ny_tree_census_runner \
self-hosted_runner /bin/bash -c "\
./config.sh \
--unattended \
--labels ubuntu,ds,no-gpu \
--url https://github.com/AlekseiBogachev/ny-tree-census \
--token $(cat .runner_secret_token) && \
./run.sh"
