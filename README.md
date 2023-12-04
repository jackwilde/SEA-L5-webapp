# myTraining

### About
myTraining is an application designed for users to log it training they have completed and allows managers to review the training their staff have logged.

### Python requirements
The application supports Python 3.11 and the required packages are listed in [requirements.txt](./requirements.txt)

### Additional Requirements
In order to run the application a connection to a postgres database is required.

### Environment
Several environment variables are required for the application to run.

| Environment Variable | Description                                                              |
|----------------------|--------------------------------------------------------------------------|
| ADMIN_FIRST_NAME     | First Name for the initial admin account created during first launch.    |
| ADMIN_LAST_NAME      | Last Name for the initial admin account created during first launch.     |
| ADMIN_EMAIL          | Email address for the initial admin account created during first launch. |
| ADMIN_PASSWORD       | Password for the initial admin account created during first launch.      |
| DB_HOST              | Hostname or IP address of Postgres server.                               |
| DB_USER              | Username of user with permission to connect to database.                 |
| DB_PASSWORD          | Password for the database user                                           |
| DB_NAME              | The name of the database within Postgres to store application data       |