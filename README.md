# d1g1t_assignment
*Environment Setup:

PyCharm Community Version was used to implement this project from scratch.
Install it from here `https://www.jetbrains.com/pycharm/download/#section=linux` 
You can clone the repository or download and open in PyCharm.

You have to create a new virtual environment. Please make sure you choose script path to the location where `manage.py` resides. 'parameters' should be `runserver`
and the working directory should be set to `../PycharmProjects/d1g1t_assignment/`.
please create a superuser for yourself with `python manage.py createsuperuser` so that you can access django admin.

Install all the requirements with `pip install -r requirements.txt`. In terminal, you should be in this directory, `/PycharmProjects/d1g1t_assignment` while doing so.

Apply all the migrations with `python manage.py migrate`.

To access django admin, cd to `/PycharmProjects/d1g1t_assignment/d1g1t_assignment`. Login with your superuser credentials.

*Problem Solution:

Only a superuser can create other django users and teams. A member will be created with that django user id and team id. A member will also have a token created
which will be unique to each member and will be used for the authentication purpose. Once a member is created via django admin by the superuser. Members of
different teams can utilize the endpoints.

We have following urls for the scenario,
1. 'http://localhost:8000/admin' (django admin)
2. 'http://localhost:8000/happiness/submit/' (POST)
3. 'http://localhost:8000/happiness/stat' (GET) [Allowed with or without token]
4. 'http://localhost:8000/happiness/member' (GET)
5. 'http://localhost:8000/happiness/team' (GET)

A member will be verified based on the provided token and provided information. A `happiness_level` can be varied from 0 to 10. 0 means `no reaction/neutral` and 10 means extremely happy. A member can provide their happiness_level in a scale of 0-10 each day. date is default to the current day unless user doesn't provide it. No matter what they submit, they are allowed to submit one rating for each day. (date and member are unique).
Everytime a member submits a `happiness_level` their `average_happiness` is calculated and stored in the `member` model.

While an unauthenticated request is made (no token provided) to the `/happiness/stat/` we just calculate the average of all the happiness_levels across all teams from the `HappinessLevel` model. If a valid token is provided, based on the members team, we get the `average_happiness` of each member of that team and increase the index of the happiness in a dictionary. We also consider all the happiness_level submissions to calculate the average of happiness in that specific team and display it.
A sample output would look like this,
```
{
    "happiness_level": {
        "0": 0,
        "1": 0,
        "2": 0,
        "3": 1,
        "4": 0,
        "5": 2,
        "6": 0,
        "7": 0,
        "8": 0,
        "9": 0
    },
    "average_happiness_of_your_team": 4.090909090909091
}
```
Note that, the member `M` who hit the endpoint will see such output. M is working in a team having 3 members. Each members average happiness is displayed in this `happiness_level`. Also, members continiously submitted their ratings over time and we calculated the average of all those ratings for that team and displayed it as `average_happiness_of_your_team`.

