# Celery-based Data Processing Application

This project is a Celery-based application that periodically fetches user data from external API, stores it in a PostgreSQL database, and supplements it with additional information such as addresses and credit card details.


## Project Overview

This application uses Celery to manage periodic tasks such as fetching user data, addresses, and credit card information. The data is fetched from the following APIs:
- [Random Data API](https://random-data-api.com/)

The application stores the fetched data in a PostgreSQL database and uses Redis as a message broker.

## Project Setup

### Prerequisites

Before you start, ensure you have the following installed:
- Docker and Docker Compose

### Configuration
Create a `.env` file in the root directory of the project using `.env.example` as a template.

### Running the Application

To run the application, use the following command:

```bash
docker compose up -d
```

This command will start the application and create the necessary containers for PostgreSQL, Redis, pgAdmin and the Celery worker.

### Accessing the Application

You can access the application at the following URLs:

- [pgAdmin](http://localhost:5050) (enter database credentials from the `.env` file)

### Stopping the Application

To stop the application, use the following command:

```bash
docker compose down
```

### Running Tests

To run the tests, use the following command:

```bash
docker compose -f docker-compose.test.yml up
```

This command will run the tests and output the results to the console.
