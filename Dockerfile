# set base image (host OS)
# Pinned to Debian 11 "bullseye". The plain `python:3.8` tag now points at
# Debian 12 "bookworm", which dropped libssl1.1. MongoDB 4.4 needs libssl1.1,
# so on bookworm `apt-get install mongodb-org` fails with broken packages.
# Bullseye still has it, so the original setup installs fine.
FROM python:3.8-bullseye

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

RUN apt-get -y update
RUN apt-get install -y curl nano wget nginx git

RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list


# Mongo
RUN ln -s /bin/echo /bin/systemctl
RUN wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | apt-key add -
RUN echo "deb http://repo.mongodb.org/apt/debian buster/mongodb-org/4.4 main" | tee /etc/apt/sources.list.d/mongodb-org-4.4.list
RUN apt-get -y update
RUN apt-get install -y mongodb-org

# Install Yarn
RUN apt-get install -y yarn

# Ensure pip is available/up to date.
# The original `easy_install pip` no longer works: `easy_install` was removed
# from modern setuptools (>=58.3), so it exits 127. pip already ships in the
# python base image, so we just upgrade it.
RUN python -m pip install --upgrade pip


ENV ENV_TYPE staging
ENV MONGO_HOST mongo
ENV MONGO_PORT 27017
##########

ENV PYTHONPATH=$PYTHONPATH:/src/

# copy the dependencies file to the working directory
COPY src/requirements.txt .

# install dependencies
RUN pip install -r requirements.txt
