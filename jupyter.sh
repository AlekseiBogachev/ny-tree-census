#!/bin/bash
./build.sh

docker run \
--rm \
-p 127.0.0.1:8080:8080 \
ny_tree_census_dev \
poetry run jupyter notebook \
--ip 0.0.0.0 \
--port 8080 \
--no-browser