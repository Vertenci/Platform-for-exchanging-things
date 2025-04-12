## Platform for exchanging things.
### Installation
- Creating a project in PyCharm
- Cloning the repository, using the command in the terminal - git clone https://github.com/Vertenci/Platform-for-exchanging-things.git
- Download Docker Desktop
- Create download postgres image
- Run container with settings:
1. Container name - my_postgres
2. Host port - 5432
3. Environment variables:
- Click the Add button and add the following variables:
1. Variable: POSTGRES_USER, Value: your username (e.g. yourusername).
2. Variable: POSTGRES_PASSWORD, Value: your password (e.g. yourpassword).
3. Variable: POSTGRES_DB, Value: your database name (e.g. yourdatabase).
- After filling in all the fields, click the Run button at the bottom of the window. The PostgreSQL container will start.
### Migrations
In the terminal, enter the commands:
- python manage.py createmigrations
- python manage.py migrate
### Starting the server
- python manage.py runserver
### Testing
- python manage.py test
