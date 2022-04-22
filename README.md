# d1g1t_assignment
*Environment Setup:

PyCharm Community Version was used to implement this project from scratch.
Install it from here https://www.jetbrains.com/pycharm/download/#section=linux 
You can clone the repository or download and open in PyCharm.

You have to create a new virtual environment. Please make sure you choose script path to the location where 'manage.py' resides. 'parameters' should be 'runserver'
and the working directory should be set to '../PycharmProjects/d1g1t_assignment/'.
please create a superuser for yourself with 'python manage.py createsuperuser' so that you can access django admin.

Install all the requirements with 'pip install -r requirements.txt'. In terminal, you should be in this directory, '/PycharmProjects/d1g1t_assignment' while
doing so.

Apply all the migrations with 'python manage.py migrate'.

To access django admin, cd to '/PycharmProjects/d1g1t_assignment/d1g1t_assignment'. Login with your superuser credentials.

*Problem Solution:

Only a superuser can create other django users and teams. A member will be created with that django user id and team id. A member will also have a token created
which will be unique to each member and will be used for the authentication purpose. Once a member is created via django admin by the superuser. Members of
different teams can utilize the endpoints.

We have following urls for the scenario,
1. 'http://localhost:8000/admin' (django admin)
2. 'http://localhost:8000/happiness/submit/' (POST)
3. 'http://localhost:8000/happiness/stat' (GET) [Allowed with or without token']
4. 'http://localhost:8000/happiness/member' (GET)
5. 'http://localhost:8000/happiness/team' (GET)



