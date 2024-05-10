
#!/bin/bash
./build.sh

echo ""
echo "Создание контейнера и запуск code-server"
echo ""

docker run \
--detach \
--name ny_tree_census_code_server \
--rm \
-p 127.0.0.1:8080:8080 \
-p 127.0.0.1:8050:8050 \
ny_tree_census_dev \
code-server \
--disable-telemetry \
--disable-update-check \
--disable-workspace-trust \
--disable-getting-started-override \
--bind-addr 0.0.0.0:8080 \
/dockeruser/ny_tree_census

sleep 1

echo "code-server is running"
echo "code-server parameters:"
docker exec -it ny_tree_census_code_server \
cat /dockeruser/.config/code-server/config.yaml

echo "\ncode-server help\n"
docker exec -it ny_tree_census_code_server \
code-server --help

# docker attach ny_tree_census_code_server