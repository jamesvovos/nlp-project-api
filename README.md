# NLP Project API.
## _Implementation using FastAPI & SQLAlchemy ORM._

![ApiImage](https://appmaster.io/api/_files/PqV7MuNwv89GrZvBd4LNNK/download/)

## Installation Guide
FastAPI installation instructions [FastAPI website](https://fastapi.tiangolo.com/)
SQLAlchemy installation instructions [FastAPI docs](https://fastapi.tiangolo.com/tutorial/sql-databases/)
Pydantic installation instructions [Pydantic website](https://docs.pydantic.dev/install/)

## 1. Install FastAPI

Install `FastAPI`
```sh
$pip install fastapi
```
## 2. Install Uvicorn

Install Uvicorn:
```sh
$pip install "uvicorn[standard]"
```

To run the server - cd/ into the project directory and run the command:
```sh
$uvicorn endpoints:app --reload
```
## 3. Install Pydantic
Install Pydantic:
```sh
$pip install pydantic
```

## Features

- API to add custom intents, tags, patterns & responses to AI model.
- API to customize AI text-to-speech responses including: tone, personality, name, voice, etc.
- Modify API endpoints to train model.
- Can be built upon later to add NLP neural net model to games (mini plugin).


## Customize
Have a look at [Postman](https://www.postman.com/) to checkout the API endpoints. Refer to the `endpoints.py` file to view/manage the API endpoints.
Customize the database schema in the `database/models.py` file. Add in your own database integrations by replacing the `SQLALCHEMY_DATABASE_URL = ''` in the `database/database.py` file. Refer to SQLAlchemy documentation for further info based on the database provider you choose.

```sh
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# establish connection database using SQLAlchemy ORM
SQLALCHEMY_DATABASE_URL = ''

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# the database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base class to create a database model/table
Base = declarative_base()
```

## License

MIT
