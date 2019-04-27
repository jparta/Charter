# Charter

A Flask microservice for registering and fetching visualizations by and for the A+ Learning Management System

## Setup
1. Install requirements
  - `pip install -r requirements.txt`
  - [Install and set up RabbitMQ](https://docs.celeryproject.org/en/latest/getting-started/brokers/rabbitmq.html) (or another message broker, just remember to update config.py)
  - Install PostgreSQL
2. Set hooks in Aplus (/admin/course/coursehook/)
  - Hook url: set the IP and port of the script server, and add the configured hook token as a parameter (?token=)

## Usage
1. Run Aplus according to its instructions
2. Run the broker from /Charter with `celery worker -A entrypoint_celery --loglevel=DEBUG`
3. Start the server from /Charter with `flask run`

## TODO
- Run everything in containers

