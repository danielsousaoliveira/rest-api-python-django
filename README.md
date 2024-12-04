# REST API Django

REST API for monitoring pollution data, built using Django and Python. Supports CRUD operations, allows filtering and pagination.
The project includes Swagger documentation and is containerized using Docker for ease of setup.

## Features

-   RESTful API with Django Rest Framework
-   Pollution data monitoring
-   CSV data import for measurements
-   Swagger and ReDoc API documentation
-   Integrated with PostgreSQL and PostGIS for geographic functionalities
-   Dockerized for easy setup and deployment

## Setup and Installation

### Option 1: Docker Setup (Recommended)

1. **Clone the repository**:

    ```bash
    git clone rest-api-python-django
    cd rest-api-python-django
    ```

2. **Build and start the Docker container**:
    ```bash
    docker-compose up --build
    ```

This command will:

-   Build the Docker image.
-   Set up the Postgres database with PostGIS extensions.
-   Apply migrations.
-   Create a superuser.
-   Import CSV data into the database.

3. **Open the API documentation in your browser**:

    - Swagger UI: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
    - Redoc: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)
    - API: [http://localhost:8000/api/](http://localhost:8000/api/)

4. **Admin panel**:

    - [http://localhost:8000/admin/](http://localhost:8000/admin/)
    - Use the super user credentials to login

5. **Running tests**:

The entrypoint already runs the tests automatically, but if you need to do it manually:

```bash
docker-compose exec web python3 manage.py test
```

### Option 2: Local Virtual Environment Setup

If you prefer to run the project without Docker, follow these steps:

1. **Clone the repository**:

    ```bash
    git clone rest-api-python-django
    cd rest-api-python-django
    ```

2. **Create and activate a virtual environment**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the dependencies**:

    ```bash
    pip3 install -r requirements.txt
    ```

4. **Set up your PostgreSQL database**:

    - Create a database and enable the PostGIS extension:

        ```sql
        CREATE DATABASE pollution_data;
        \c pollution_data
        CREATE EXTENSION postgis;
        ```

    - In your project, create a `.env` file with the following content:
        ```env
        DB_NAME=pollution_data
        DB_USER=your_db_username
        DB_PASSWORD=your_db_password
        DB_HOST=localhost
        DB_PORT=5432
        ```

5. **Apply database migrations**:

    ```bash
    python3 managy.py makemigrations
    python3 manage.py migrate
    ```

6. **Create a superuser**:

    ```bash
    python3 manage.py createsuperuser
    ```

7. **Run the development server**:

    ```bash
    python3 manage.py runserver
    ```

8. **Open the API documentation in your browser**:

    - Swagger UI: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
    - Redoc: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)
    - API: [http://localhost:8000/api/](http://localhost:8000/api/)

9. **Admin Panel**:

    - [http://localhost:8000/admin/](http://localhost:8000/admin/)
    - Use the credentials you created with `createsuperuser` to log in.

10. **Running Unit Tests**

To run the unit tests, use the following command:

```bash
python3 manage.py test
```

## Roadmap

[x] ~~Create REST API with CRUD operations~~ \
[x] ~~Create unit tests~~ \
[x] ~~Add pagination and filtering~~ \
[ ] Integrate pollution sensors

## References

-   [Django](https://www.djangoproject.com/start/)
-   [Django Rest Framework](https://www.django-rest-framework.org/)
-   [Docker](https://docs.docker.com/get-started/)
-   [PostGIS](https://postgis.net/documentation/getting_started/)
-   [Swagger Generator](https://drf-yasg.readthedocs.io/en/stable/)
-   [Django Filters](https://django-filter.readthedocs.io/en/stable/)
