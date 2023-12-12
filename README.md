# myTraining

## About
myTraining is a Python based web application using the Flask framework. It provides a platform for users to log any IT
based training that they have completed. 

## Getting started
### Python Setup
The application is written and tested with Python 3.11 and the packages required to run it are listed in the
[requirements.txt](./requirements.txt) file.

### Database
A PostgreSQL database is required for this application to store its data. A database should be created on the PostgreSQL
server along with a database user who can perform all CRUD actions within that database. The database connection
settings are read by the application from system environment variables.

### Environment
The following environment variables are required in order to run the application.

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


### Run the application
A Web Server Gateway Interface (WSGI) is required to run Flask applications and so should also be installed on the
server hosting the myTraining application.

## Using the application
### Roles
The myTraining application has two roles
* Standard
* Admin

During the first launch the application will create an admin user from the details set via environment variables. This
admin user can then be used to promote other users to the admin role. Otherwise all users who create an account via the
sign up page will become standard users.

### Standard Users
Standard users are able to log into the application to log any training they have completed. They are also permitted to
view and update any of their own training.

### Admin Users
Admin users can use the same functions as standard users but will also have access to admin functions. These will allow
them to do the following actions:
* Create, read, update, and delete users
* Create, read, update, and delete training
* View training logged for a given user
* View training logged for a given category
