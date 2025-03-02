# FlaskProject1

A sample project using Flask, SQLAlchemy, and Poetry.

## Description

This project is a simple Flask application that demonstrates the use of Flask 
with SQLAlchemy for database operations. It includes basic CRUD operations
for managing tasks.

## Features

- Create, list, complete, and delete tasks
- Error handling for database operations
- Unit tests for service functions
- Parameterised tests with pytest

## Requirements

- Python 3.12 or higher
- Poetry for dependency management

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/your-repo/flaskproject1.git
    cd flaskproject1
    ```

2. Install dependencies using Poetry:

    ```sh
    poetry install
    ```

3. Set up the database:

    ```sh
    poetry run flask db upgrade
    ```

## Usage

1. Run the Flask application:

    ```sh
    poetry run flask run
    ```

2. Access the application at `http://127.0.0.1:5000`.

## Running Tests

To run the tests, use the following command:

```sh
poetry run pytest
```

## Project Structure

- `app/`: Contains the application code
  - `models.py`: Defines the database models
  - `services.py`: Contains the service functions for task operations
  - `__init__.py`: Initializes the Flask application
- `tests/`: Contains the unit tests
- `migrations/`: Contains the database migration files
- `run.py`: Entry point for running the Flask application
- `pyproject.toml`: Configuration file for Poetry

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
