from django.test import TestCase
from django.db.models import Avg
from django.contrib.auth.models import User
from django.test.client import Client
from .models import Team, Member, HappinessLevel

class HappinessTestCase(TestCase):
    """ Test module for Puppy model """

    def setUp(self):
        password = 'password'
        admin = User.objects.create_superuser('admin', 'admin@test.com', password)
        c = Client()
        c.login(username=admin.username, password=password)
        # Teams creation
        t1 = Team.objects.create(name='alpha')
        t2 = Team.objects.create(name='beta')
        t3 = Team.objects.create(name='gamma')

        # Django Users and members Creation
        u1 = User.objects.create_user(username='mike', email='mike@test.com', password=password)
        Member.objects.create(member=u1, name="Mike Tyson", team=t1)
        u2 = User.objects.create_user(username='jack', email='jack@test.com', password=password)
        Member.objects.create(member=u2, name="Jack Daniels", team=t1)
        u3 = User.objects.create_user(username='richard', email='richard@test.com', password=password)
        Member.objects.create(member=u3, name="Richard Park", team=t1)
        u4 = User.objects.create_user(username='sara', email='sara@test.com', password=password)
        Member.objects.create(member=u4, name="Sara Smith", team=t2)
        u5 = User.objects.create_user(username='ashley', email='ashley@test.com', password=password)
        Member.objects.create(member=u5, name="Ashley Monks", team=t2)
        u6 = User.objects.create_user(username='nicole', email='nicole@test.com', password=password)
        Member.objects.create(member=u6, name="Nicole Graham", team=t3)


    def testMemberView(self):
        url = '/happiness/member/'
        c = Client()
        # Trying to access endpoint without any token
        response = c.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'valid token required')

        # grab a valid token representing a member.
        # This time it should show the member information
        m = Member.objects.get(name='Nicole Graham')
        response = c.get(url+'?token={}'.format(m.token))
        self.assertEqual(response.status_code, 200)

        # make sure the token actually filters out the right member
        self.assertEqual(response.json()['name'], m.name)

        # an invalid token provided. Should get http 400.
        response = c.get(url+'?token=wrongtoken')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'provided token is invalid')

    def testTeamView(self):
        url = '/happiness/team/'
        c = Client()
        # Trying to access endpoint without any token
        response = c.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'valid token required')

        # grab a valid token representing a member.
        # This time it should show the team information
        m = Member.objects.get(name='Ashley Monks')
        response = c.get(url + '?token={}'.format(m.token))
        self.assertEqual(response.status_code, 200)

        # make sure team information are displayed
        self.assertEqual(response.json()[0]['name'], 'alpha')
        self.assertEqual(response.json()[1]['name'], 'beta')
        self.assertEqual(response.json()[2]['name'], 'gamma')

        # an invalid token provided. Should get an http 400.
        response = c.get(url + '?token=wrongtoken')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'provided token is invalid')

    def testhappinesslevelSubmitandView(self):
        # we are testing the daily happiness submission and viewing
        # statistical information step by step
        url = '/happiness/submit/'
        c = Client()

        # post request without token is not allowed
        response = c.post(url, data={}, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'token is required')

        # even invalid token won't allow posting anything
        data = {"token": 'abc'}
        response = c.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'provided token is not valid')

        # Mike from team alpha is submitting his happiness for a day
        m1 = Member.objects.get(name="Mike Tyson")
        data = {
            "token": m1.token,
            "date": "2022-04-01",
            "happiness_level": 4
        }
        response = c.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['member'], m1.id)
        self.assertEqual(response.json()['happiness_level'],
                         data['happiness_level'])

        # Mike is trying to post another happiness_level for the same
        # day. It won't be allowed.
        data['happiness_level'] = 6
        response = c.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {'non_field_errors': ['The fields member, date must make a unique set.']})

        # Mike is posting his happiness level for second day
        data = {
            "token": m1.token,
            "date": "2022-04-02",
            "happiness_level": 5
        }
        response = c.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)

        # Mike is posting his happiness level for third day
        data = {
            "token": m1.token,
            "date": "2022-04-03",
            "happiness_level": 9
        }
        response = c.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)

        # Mike has posted happiness_level for three days. Now,
        # we will verify the average_happiness of Mike
        m1.refresh_from_db()
        avg_happiness = list(HappinessLevel.objects.filter(member=m1).aggregate(Avg('happiness_level')).values())[0]
        self.assertEqual(avg_happiness, m1.average_happiness)

        # Posting happiness_level for Jack from alpha team
        m2 = Member.objects.get(name='Jack Daniels')
        # Jack is posting his happiness level for second day
        data = {
            "token": m2.token,
            "date": "2022-04-01",
            "happiness_level": 4
        }
        response = c.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)

        # Jack is posting his happiness level for third day
        data = {
            "token": m2.token,
            "date": "2022-04-02",
            "happiness_level": 8
        }
        response = c.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)

        # Jack has posted happiness_level for two days. Now,
        # we will verify the average_happiness of Jack
        m2.refresh_from_db()
        avg_happiness = list(HappinessLevel.objects.filter(member=m2).aggregate(Avg('happiness_level')).values())[0]
        self.assertEqual(avg_happiness, m2.average_happiness)

        # post for Richard who is also from alpha
        m3 = Member.objects.get(name='Richard Park')
        # Richard is posting his happiness level for a day
        data = {
            "token": m3.token,
            "date": "2022-04-01",
            "happiness_level": 4
        }
        response = c.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        m3.refresh_from_db()

        # We will post one more happiness_level from a different team beta
        # for Sara
        m4 = Member.objects.get(name='Sara Smith')
        # Sara is posting his happiness level for a day
        data = {
            "token": m4.token,
            "date": "2022-04-01",
            "happiness_level": 10
        }
        response = c.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        m4.refresh_from_db()

        url = '/happiness/stat/'
        # post request without a token will just display
        # the average happiness across all teams
        response = c.get(url, content_type='application/json')
        avg_happiness_all_teams = list(HappinessLevel.objects.all().aggregate(Avg('happiness_level')).values())[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(avg_happiness_all_teams, response.json()["average_happiness_across_all_teams"])

        # Mike is from team alpha. There are two members
        # at happiness level 6 and one member at level 4.
        # we caluclate the average_happiness of the team averaging all
        # the happiness_levels of the members.

        m = Member.objects.get(name='Mike Tyson')
        response = c.get(url + '?token={}'.format(m.token))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['happiness_level'],
              {'0': 0, '1': 0, '2': 0, '3': 0, '4': 1, '5': 0, '6': 2, '7': 0, '8': 0, '9': 0})
        members_of_same_team = Member.objects.filter(team=m.team)
        avg_happiness_of_same_team = list(HappinessLevel.objects.filter(
            member__in=members_of_same_team).aggregate(Avg('happiness_level')).values())[0]
        self.assertEqual(response.json()['average_happiness_of_your_team'], avg_happiness_of_same_team)
