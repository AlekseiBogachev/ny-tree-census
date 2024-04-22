
#!/bin/bash
./build.sh

docker run \
--detach \
--name ny_tree_census_code_server \
--rm \
-p 127.0.0.1:8080:8080 \
ny_tree_census_dev \
code-server --bind-addr 0.0.0.0:8080 /dockeruser/ny_tree_census

sleep 1

echo "code-server parameters:"
docker exec -it ny_tree_census_code_server \
cat /dockeruser/.config/code-server/config.yaml

docker attach ny_tree_census_code_server