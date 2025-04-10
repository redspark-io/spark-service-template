# spark-service-template

This is a template for building microservices using FastAPI and hexagonal architecture (also known as ports and adapters architecture).

## Project Structure

```
src/
├── application/        # Application layer (use cases)
│   ├── ports/         # Interface definitions
│   └── use_cases/     # Business logic implementation
├── domain/            # Domain layer (business entities)
│   └── entities/
└── infrastructure/    # Infrastructure layer
    ├── adapters/      # Implementation of ports
    └── api/           # API endpoints
```

## Requirements

- Python 3.9+
- Poetry for dependency management

## Dependencies and Versions

### Main Dependencies

- FastAPI (^0.104.1)
- Uvicorn (^0.24.0)
- Pydantic (^2.4.2)
- Pydantic-Settings (^2.0.3)

### Development Dependencies

- pytest (^7.4.3)
- pytest-cov (^4.1.0)
- black (^23.10.1)
- isort (^5.12.0)
- flake8 (^6.1.0)
- mypy (^1.6.1)
- pre-commit (^3.5.0)
- pyspelling (^2.9.0)

## Setup

1. Install Poetry:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies:

```bash
poetry install
```

3. Install pre-commit hooks:

```bash
poetry run pre-commit install
```

## Environment and Dependency Management

### Check if the virtual environment is active

```bash
poetry env info
```

### Enter the virtual environment

```bash
poetry shell
```

### Add a new dependency

Example: Add `requests` to the project.

```bash
poetry add requests
```

To add only to the development environment:

```bash
poetry add requests --group dev
```

### Remove a dependency

```bash
poetry remove requests
```

### Update all dependencies

```bash
poetry update
```

Update a specific dependency:

```bash
poetry update fastapi
```

## Development

### Run the application:

```bash
poetry run uvicorn src.infrastructure.api.main:app --reload
```

### Run tests:

```bash
poetry run pytest
```

### Run the project (if main.py is the entry point):

```bash
poetry run python src/infrastructure/api/main.py
```

### Run code formatting:

```bash
poetry run black .
poetry run isort .
```

### Run type checking:

```bash
poetry run mypy src
```

### Run spell checking:

```bash
poetry run pyspelling
```

## Git Hooks

The project includes pre-commit hooks that:

- Run unit tests
- Check code formatting (black, isort)
- Run linting (flake8)
- Check types (mypy)
- Check spelling

These checks must pass before commits can be pushed to the repository.

### Run hooks manually

```bash
poetry run pre-commit run --all-files
```

## Debugging and Diagnostics

### Check the consistency of pyproject.toml

```bash
poetry check
```

### List all installed dependencies

```bash
poetry show
```

For details of a specific package:

```bash
poetry show fastapi
```

### Debug dependencies (resolve conflicts)

```bash
poetry debug resolve
```

## API Documentation

Once the application is running, you can access:

- API documentation: http://localhost:8000/docs
- OpenAPI specification: http://localhost:8000/openapi.json

## Code Style

This project follows these code style guidelines:

- Black for code formatting (line length: 88 characters)
- isort for import sorting (configured to be compatible with Black)
- Flake8 for code linting
- MyPy for static type checking

## License

MIT

> > > > > > > master
