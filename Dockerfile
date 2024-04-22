ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}

ARG UNAME=dockeruser
ARG UID=1001
ARG GID=1001
ARG GITUSER="Aleksei Bogachev"
ARG GITEMAIL="bogachev.aleksey.m@gmail.com"

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

RUN curl -fsSL https://code-server.dev/install.sh | sh

USER ${UNAME}

RUN git config --global user.name "${GITUSER}"
RUN git config --global user.email "${GITEMAIL}"

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/${UNAME}/.local/bin:/.local/bin:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN poetry config installer.max-workers 10

WORKDIR /${UNAME}/ny_tree_census
COPY poetry.loc[k] pyproject.toml /${UNAME}/ny_tree_census/
RUN poetry install --no-root

CMD /bin/bash
