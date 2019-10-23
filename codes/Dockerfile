
###########
# BUILDER #
###########

# pull official base image
FROM python:3.7.0-alpine as builder

# set work directory
WORKDIR /usr/src/codes

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# lint
RUN pip install --upgrade pip
RUN pip install flake8
COPY . /usr/src/codes/
RUN flake8 --ignore=E501,F401 .

# install dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/codes/wheels -r requirements.txt

#########
# FINAL #
#########

# pull official base image
FROM python:3.7.0-alpine

# create directory for the codes user
RUN mkdir -p /home/codes/

# create the app user
RUN addgroup -S codes && adduser -S codes -G codes

# create the appropriate directories
ENV HOME=/home/codes
ENV APP_HOME=/home/codes/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# install dependencies
RUN apk update && apk add libpq
COPY --from=builder /usr/src/codes/wheels /wheels
COPY --from=builder /usr/src/codes/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# copy entrypoint
COPY entrypoint.sh $APP_HOME

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R codes:codes $APP_HOME

# change to the app user
USER codes

# run entrypoint.prod.sh
ENTRYPOINT ["/home/codes/web/entrypoint.sh"]
