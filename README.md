# madlibs-demo

This is a demo project demonstrating creating a madlib sentence based on calling an api to get different word types.

## Run

If you have the docker image built already just run the following and visit [https://localhost:8000](https://localhost:8000)

```
$ docker run -it --name madlibs --rm -p 8000:8000 madlibs:latest
```

## Development

It is recommended to use `asdf-vm` for python version managment. There is a `.tool-versions` file to autoswitch to the proper project python version.

### Setup

To get up and running for either development or running tests do the following after cloneing the repo.

```
$ cd madlibs
$ python -m venv .venv --prompt=madlibs
$ source .venv/bin/activate
$ pip install -r requirements/test.txt
```

### Run Tests

Running a simple pytest command sets everything off well.

```
DJANGO_SETTINGS_MODULE=config.settings.test pytest
```

### Build Docker Image

Build image for either local testing or pusing to a repository.

```
docker build . -t madlibs:latest
```
