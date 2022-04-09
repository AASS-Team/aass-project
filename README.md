# AASS Project

![master pipeline](https://github.com/MCFreddie777/aass-project/actions/workflows/github-ci.yml/badge.svg?branch=master)

## Prerequisites

- [Docker](https://www.docker.com/)

## Installation and configuration

1. Set your environment variables by creating your own `.env` file in root similar to `.env.example`.

    - Specify `DJANGO_SECRET_KEY`. It can be generated as `base64 /dev/urandom | head -c50`.

   All Other configuration in `.env.example` is ready for local development.

2. Build and run docker containers

   Run following command in base directory of this project:

    ```
    docker-compose up --build -d
    ```

   Docker image for this application will be automatically built. Then, all necessary infrastructure (e.g. database)
will be run along with web application.

3. Run database migrations

   Create all necessary tables in database by executing:

    ```
    docker-compose exec web pipenv run migrate
    ```

4. Optional: Seeding the database with fake data

    ```
	docker-compose exec web pipenv run seed
    ```

## Usage

- Run `docker-compose up` in base directory of this project.
- Visit `http://localhost:8000` in your browser.
- To stop the server, use `docker-compose down`

### Code formatting

Before committing, format code using `black` formater:

```
docker-compose exec web pipenv run lint
```

### Unit tests

Run unit tests using following command:

```
docker-compose exec web pipenv run test
```

