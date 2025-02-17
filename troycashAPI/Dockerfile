FROM python:3.12-bullseye

ENV IS_DOCKER_BUILD="1"
ENV HOME="/root"
ENV PROJECT_DIR="/app"

WORKDIR ${PROJECT_DIR}

# not copying the source code, when needed directly mounting the files.
COPY . .

# Switch to bash shell
# SHELL ["/bin/bash", "-c"]

RUN pip install -r requirements.txt

RUN pip install --upgrade pip

# RUN pip install --no-cache-dir -U setuptools

CMD ["entrypoint.sh"]