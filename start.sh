#!/bin/bash

echo ""
echo "Сборка образов"
echo ""

./build_runner.sh
./build_dev_env.sh


echo ""
echo "Создание и запуск контейнеров"
echo ""

./start_runner.sh
./start_code-server.sh
