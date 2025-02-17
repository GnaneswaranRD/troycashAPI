FROM python:3.12-bullseye

ENV IS_DOCKER_BUILD="1"
ENV HOME="/root"
ENV PROJECT_DIR="/app"

WORKDIR ${PROJECT_DIR}

# not copying the source code, when needed directly mounting the files.
COPY . .

# Switch to bash shell
# SHELL ["/bin/bash", "-c"]

RUN pip install -r requirements.txt && pip install --upgrade && pip install -U setuptools

CMD ["entrypoint.sh"]