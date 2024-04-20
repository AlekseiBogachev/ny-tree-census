# Описание CI/CD конвейера

## Основные шаги

Описание CI/CD конвейера находится в файле
[/.github/workflows/test_and_lint.yaml](/.github/workflows/test_and_lint.yaml)
(каталог проекта считать корневым).

Укрупнённо основные этапы CI/CD приведены на диаграмме ниже. На диаграмме для
каждого этапа подписан его job из
[test_and_lint.yaml](/.github/workflows/test_and_lint.yaml).

![Этапы ci/cd](/docs/figures/cicd_stages.svg)

Сейчас конвейер не содержит ни автотестов (шаг с автотестами выводит сообщение
о том, что тестов нет), ни шагов, связанных с обучением и оценкой моделей.
Возможно, эти этапы будут добавлены позже.

## Self-hosted runner

### Структура и основные этапы работы

[Self-hoted runner](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners)
позволяет выполнять задачи CI/CD на собственной вычислительной машине будь то
локальная рабочая станция, удалённая арендованная виртуальная машина или
docker-контейнер.

Такой подход даёт несколько преимуществ:

- использование CI/CD с GitHub Actions для тестирования
и обучения моделей без ограничений бесплатных GitHub-hosted
runners;
- использование GPU для обучения моделей.

В проекте реализован запуск
[self-hoted runner](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners)
в Docker-контейнере, что позволяет изолировать его от локальной машины, а также
упрощает и унифицирует процесс развёртывания, то есть его можно будет перенести
на удалённую виртуальную машину в облаке.

Структура
[self-hoted runner](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners)
показана на рисунке ниже.

![Структура self-hosted runner](/docs/figures/self-hosted_runner_container.svg)

Базовым образом для контейнера с
[self-hoted runner](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners)
служит базовый образ [`ny_tree_census_base`](/docs/development_environment.md),
поэтому прежде чем собирать образ для
[self-hoted runner](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners)
и запускать его, нужно собрать базовый образ.
Подробнее в следющем разделе и разделе
[Среда разработки](/docs/development_environment.md).

### Сборка образа, запуск runner-а и его остановка

> [!IMPORTANT]
> Для регистрации
> [self-hoted runner](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners)
> в GitHub Actions необходимо получить временный токен (подробнее про это в
> [Adding self-hosted runners](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/adding-self-hosted-runners)). Токен нужно
> скопировать в файл `/gh_actions_runner/.secret_token`.
> **Нужно скопировать только токен, а не всю команду!**

После того как базовый образ `ny_tree_census_base` собран, а токен добавлен,
можно собрать образ для
[self-hoted runner](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners)
с помощью скрипта [build_runner.sh](/gh_actions_runner/build_runner.sh).
Для этого нужно из корневого каталога репозитория выполнить следующую команду:

```shell
user@user-pc:~/Project$ ./gh_actions_runner/build_runner.sh
```

Скрипт [build_runner.sh](/gh_actions_runner/build_runner.sh) собирает образ
контейнера из [Dockerfile](/gh_actions_runner/Dockerfile), расположенного по
адресу `/gh_actions_runner/Dockerfile`

Сборка образа раннера состоит из следующих этапов:

1. Берется локальный базовый образ `ny_tree_census_base`.
2. Пользователь переключается на `root`.
3. Устанавливаются недостающие пакеты.
4. Скачивается и извлекается из архива пакет с раннером.
5. Устанавливаются зависимости приложения раннера.
6. Устанавливается приложение раннера.
7. Для всех файлов и подкаталогов в каталоге `/dockeruser` рекурсивно
владелец меняется на `dockeruser`.
8. Пользователь переключается обратно на `dockeruser`.
9. На всякий случай, производится доустановка пакетов из файлов `poetry.lock`
   (если он есть в каталоге) и `pyproject.toml`, который прежде копируется из
   каталога проекта.
10. Командой по умолчанию назначается вызов Bash (`/bin/bash`).

> [!IMPORTANT]
> Нужно иметь в виду, что скрипт
> [build_runner.sh](/gh_actions_runner/build_runner.sh) соберёт контейнер даже,
> если токен для регистрации не указан или просрочен.

Регистрация и запуск
[self-hoted runner](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners)
происходят при выполнении скрипта
[start_runner.sh](/gh_actions_runner/start_runner.sh).
Скрипт [start_runner.sh](/gh_actions_runner/start_runner.sh) запустит контейнер,
прочитает токен из файла `/gh_actions_runner/.secret_token`, зарегистрирует и
запустит runner. Для запуска
[start_runner.sh](/gh_actions_runner/start_runner.sh) нужно из корневого
каталога репозитория выполнить следующую команду:

```shell
user@user-pc:~/Project$ ./gh_actions_runner/start_runner.sh
```

> [!IMPORTANT]
> Скрипт [start_runner.sh](/gh_actions_runner/start_runner.sh) присваивает 
> новому раннеру имя `ubuntu-ds-runner` и в случае, если раннер с таким именем
> уже зарегистрирован, он будет заменён новым.

[start_runner.sh](/gh_actions_runner/start_runner.sh) запускает контейнер,
который не возвращает управление пользователю, поэтому последующие операции
нужно будет выполнять из отдельного терминала.

Для удаления регистрации раннера и его остановки нужно выполнить скрипт
[remove_runner.sh](/gh_actions_runner/remove_runner.sh). Скрипт удалит
регистрацию созданного раннера `ubuntu-ds-runner`, после чего контейнер с
раннером сам остановится. Для запуска
скрипта [remove_runner.sh](/gh_actions_runner/remove_runner.sh) нужно из
корневого каталога репозитория выполнить следующую команду:

```shell
user@user-pc:~/Project$ ./gh_actions_runner/remove_runner.sh
```

> [!IMPORTANT]
> **Для удаления регистрации с помощью
> [remove_runner.sh](/gh_actions_runner/remove_runner.sh) файл
> `/gh_actions_runner/.secret_token` должен содержать актуальный токен.**
> Подробнее про удаление регистрации в
> [Removing self-hosted runners](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/removing-self-hosted-runners).

После остановки контейнер с раннером удаляется.
