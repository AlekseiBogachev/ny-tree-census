ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION} as ny_tree_census_base

ARG UNAME=dockeruser
ARG UID=1001
ARG GID=1001

USER root

RUN groupadd \
    --gid ${GID} \
    --non-unique \
    ${UNAME}

RUN useradd \
    --create-home \
    --gid ${GID} \
    --home /${UNAME} \
    --non-unique \
    --shell /bin/bash \
    --uid ${UID} \
    ${UNAME}

RUN curl \
-o quarto.deb \
-L https://github.com/quarto-dev/quarto-cli/releases/download/\
v1.5.43/quarto-1.5.43-linux-amd64.deb && \
dpkg -i quarto.deb && \
rm -rf quarto.deb

USER ${UNAME}
WORKDIR /${UNAME}/ny_tree_census

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/${UNAME}/.local/bin:/.local/bin:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN poetry config installer.max-workers 10

COPY --chown=${UNAME} pyproject.toml /${UNAME}/ny_tree_census/
RUN poetry run quarto check

CMD /bin/bash


FROM ny_tree_census_base as ny_tree_census_packages

USER ${UNAME}
WORKDIR /${UNAME}/ny_tree_census

COPY --chown=${UNAME} poetry.loc[k] pyproject.toml /${UNAME}/ny_tree_census/
RUN poetry install --no-root

RUN poetry run quarto check

CMD /bin/bash


FROM ny_tree_census_packages as ny_tree_census_dev

ARG GITUSER="Aleksei Bogachev"
ARG GITEMAIL="bogachev.aleksey.m@gmail.com"
ARG REPO="AlekseiBogachev/ny-tree-census.git"

WORKDIR /${UNAME}/ny_tree_census

USER root
RUN curl -fsSL https://code-server.dev/install.sh | sh -s -- --version=4.23.1

USER ${UNAME}

COPY --chown=${UNAME} .code-server/machine_settings.json /${UNAME}/.local/share/code-server/Machine/settings.json
COPY --chown=${UNAME} .code-server/user_settings.json /${UNAME}/.local/share/code-server/User/settings.json
COPY --chown=${UNAME} .code-server/extensions.txt /${UNAME}/ny_tree_census/.code-server/extensions.txt
RUN for EXT in $(cat /${UNAME}/ny_tree_census/.code-server/extensions.txt); \
do code-server --install-extension $EXT; \
done

COPY --chown=${UNAME} .git/ /${UNAME}/ny_tree_census/.git/
COPY --chown=${UNAME} .pre-commit-config.yaml /${UNAME}/ny_tree_census/
RUN poetry run pre-commit install --install-hooks --overwrite

COPY --chown=${UNAME} . /${UNAME}/ny_tree_census

RUN poetry install

RUN --mount=type=secret,id=pat,uid=${UID} \
git remote set-url origin \
https://$(cat /run/secrets/pat)@github.com/${REPO} && \
git config --global user.name "${GITUSER}" && \
git config --global user.email "${GITEMAIL}"

CMD /bin/bash


FROM ny_tree_census_base as gh_actions_runner

USER root
WORKDIR /${UNAME}/ny_tree_census

RUN apt-get update -y && apt install curl libdigest-sha-perl libssl3 -y

RUN curl \
-o actions-runner-linux-x64-2.316.1.tar.gz \
-L https://github.com/actions/runner/releases/download/v2.316.1/actions-runner-linux-x64-2.316.1.tar.gz && \
echo "d62de2400eeeacd195db91e2ff011bfb646cd5d85545e81d8f78c436183e09a8  actions-runner-linux-x64-2.316.1.tar.gz" | \
shasum -a 256 -c && \
tar xzf ./actions-runner-linux-x64-2.316.1.tar.gz && \
./bin/installdependencies.sh && \
rm -rf actions-runner-linux-x64-2.316.1.tar.gz

RUN chown -R ${UNAME} /${UNAME}/ny_tree_census

USER ${UNAME}
CMD /bin/bash
