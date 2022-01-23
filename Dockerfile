FROM python:3.9-alpine

EXPOSE 8000

# Create working directy for installing project
RUN mkdir -p /opt/build
WORKDIR /opt/build

# Copy the base.txt and prod.txt requirements files for install
# so that we don't redo dep install on every build.
COPY madlibs/requirements/* ./

# Install deps and cleanup afterwards to reduce container size
RUN \
    apk add --no-cache --virtual .build-deps make gcc curl musl-dev && \
    python3 -m pip install --upgrade pip && \
    python3 -m pip install -r prod.txt --no-cache-dir && \
    apk --purge del .build-deps

WORKDIR /opt
RUN rm -rf build

# Bring in the latest from the project
COPY madlibs ./

CMD ["gunicorn", "config.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]