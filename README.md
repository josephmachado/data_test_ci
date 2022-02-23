# Automate data testing as part of a CI pipeline

## Project overview

## Setup

### Pre-requisites

1. [Docker](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/) v1.27.0 or later.
2. [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

We have a [`Makefile`](Makefile) with common commands. These are executed in the running container.

```bash
git clone
cd data_test_ci
make up # starts all the containers
make ci # runs formatting, lint check, type check and python test
```

## Tear down

You can spin down the postgres and python containers using the below command.

```bash
make down
```
