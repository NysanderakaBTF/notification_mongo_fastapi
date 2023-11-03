# Test task notifications, mongoDB

### Used stack (explanation)
Python 3.11 - stable and new version of Python, supported by required libraries

FastAPI - Fast and fully asynchronous web framework

Motor - asynchronous driver for MongoDB

### Launch

First, modify env file according to your environment and smtp settings.

For running app there is a Dockerfile that contains all nessesary configuration, but database must 
be configured and run before starting the app

For full environment (DB + App) there is a docker-compose.yml file.

SwaggerUI will be available at /docs route.