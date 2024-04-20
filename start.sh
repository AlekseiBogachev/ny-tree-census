#!/bin/bash
./build.sh

docker run \
--rm \
-it \
ny_tree_census_dev \
$@
