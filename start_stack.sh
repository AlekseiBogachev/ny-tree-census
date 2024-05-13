#!/bin/bash

echo "" | tee -a ./logs/compose.log
echo "Запуск полного стека среды разработки с Docker Compose" \
| tee -a ./logs/compose.log
echo "" | tee -a ./logs/compose.log

BUILDKIT_PROGRESS=plain \
docker compose up \
--detach \
| tee -a ./logs/compose.log

sleep 1

echo "code-server is running"
echo "code-server parameters:"
docker compose exec code-server cat /dockeruser/.config/code-server/config.yaml
