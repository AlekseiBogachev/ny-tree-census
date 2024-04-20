FROM ny_tree_census_base

USER root

RUN apt-get update -y && apt install curl libdigest-sha-perl libssl3 -y

RUN curl -o actions-runner-linux-x64-2.315.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.315.0/actions-runner-linux-x64-2.315.0.tar.gz
RUN echo "6362646b67613c6981db76f4d25e68e463a9af2cc8d16e31bfeabe39153606a0  actions-runner-linux-x64-2.315.0.tar.gz" | shasum -a 256 -c
RUN tar xzf ./actions-runner-linux-x64-2.315.0.tar.gz
RUN ./bin/installdependencies.sh

ARG UNAME=dockeruser
RUN chown -R $UNAME /$UNAME
USER $UNAME

COPY poetry.loc[k] pyproject.toml ./
RUN poetry install --no-root

CMD /bin/bash
