# Template repository for FastAPI microservices

This is a template to use as a starting point for FastAPI microservice repositories. Once configured, it will run the tests on every pull request to `main`, and will automatically deploy to corresponding Heroku app when a push to `main` occurs.

## To Do after fork/create-from-template

- Simply go to the repository settings, _Actions secrets_ and create a new _repository secret_ with name `HEROKU_APP_NAME` and the name of the Heroku app in the _value_ field.
- Then, replace in `.github/workflows/deploy.yml` the `HD_X_API_KEY` value for a specific microservice secret, and the other secrets if necessary.

In the `app` directory there's a very simple example of a FastAPI app with tests.

## Local development

- First, create a `.env` file to reduce commands length, setting up the COMPOSE_PROFILES variable to "dev" (`echo COMPOSE_PROFILES=dev >> .env`)
- It's also recommended to build the container after a pull: `docker-compose build`.
- Then you can run the app: `docker-compose up`. It will also run a postgres container for development.

The app will start at port 8000 as default. You can use a specific port by setting the PORT env variable either at the `.env` file or within each command.

### Changes to database models

To create database migrations for changes done in _models_ files, run `docker-compose exec development alembic revision --autogenerate -m "Title of migration"`.

To apply changes to existing-running container, you can either restart it (`docker-compose restart`) or run the migrations (`docker-compose exec development alembic upgrade head`).

## Tests

To run the tests, simply execute `docker-compose --profile test up`. You can add `--exit-code-from test` to pass the exit code of the test script to the shell session.

Again, it's recommended to build the container after a pull. In this case, you must build with the _test_ profile: `docker-compose --profile test build`.

## Docs

The documentation is generated automatically by FastAPI. It's available in the server at `/docs` (Swagger) and `/redoc` (ReDoc)
