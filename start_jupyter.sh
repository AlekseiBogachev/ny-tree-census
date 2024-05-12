#!/bin/bash

echo ""
echo "Создание контейнера и запуск Jupyter Notebook"
echo ""

docker run \
--detach \
--name jupyter_notebook \
--rm \
-p 127.0.0.1:8080:8080 \
ny_tree_census_dev \
poetry run jupyter notebook \
--ip 0.0.0.0 \
--port 8080 \
--no-browser

sleep 3

echo $(docker logs jupyter_notebook)