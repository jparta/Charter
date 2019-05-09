# Charter

A Flask microservice for registering and fetching visualizations by and for the A+ Learning Management System

## Setup
1. Install requirements
  - `pip install -r requirements.txt`
  - Install Docker Compose and PostgreSQL
2. Set config in Charter/instance
  - In config.DevelopmentConfig, set hook and API tokens
    (find the API token from )
3. Set hooks in Aplus (/admin/course/coursehook/)
  - Hook url: set the IP and port of the script server, and add the configured hook token as a parameter (?token=)

## Usage
1. Run Aplus according to its instructions
2. Run the pack of services (Charter, RabbitMQ, Celery)
3. Go to http://localhost:5000/chart/query
4. Return an exercise in Aplus and see output in Compose

## TODO
- Use a ready compose package for these services (by Jaakko)
- Implement Aplus coordination using official protocols
- Use volumes
- Use credentials in RabbitMQ etc.
