
from rest_framework import status
from rest_framework.decorators import  api_view
from rest_framework.response import Response

from django.db.models import Avg
from .models import Team,HappinessLevel,Member
from .serializers import TeamSerializer, HappinessLevelSerializer,\
    MemberSerializer


@api_view(['POST'])
def happinessSubmit(request):
    """
    A member can submit daily happiness level through this
    post endpoint. A valid token is required to submit
    the happiness level. Level can be varied from 0 to 10.
    """
    if 'token' not in request.data:
        return Response('token is required',
                        status=status.HTTP_400_BAD_REQUEST)
    else:
        member = Member.objects.filter(token=request.data['token']).first()
        if not member:
            return Response('provided token is not valid',
                            status=status.HTTP_400_BAD_REQUEST)

        data = {"member": member.id,
                "happiness_level": request.data['happiness_level']}

        if 'date' in request.data:
            data['date'] = request.data['date']

    serializer = HappinessLevelSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        # we just calculate the average happiness of a member here.
        avg_happiness= list(HappinessLevel.objects.filter(
            member=member).aggregate(Avg('happiness_level')).values())[0]
        member.average_happiness = avg_happiness
        member.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def happinessStatistics(request):
    """
    Case 1: An authenticated user with valid token can see their team's
    average happiness level and also the frequency of happiness level.
    """
    if 'token' in request.query_params:
        member = Member.objects.filter(token=request.query_params['token']).first()
        if member:
            members_of_same_team = Member.objects.filter(team=member.team)
            happy_meter = {}
            for i in range(10):
                happy_meter[i] = 0
            for m in members_of_same_team:
                happy_meter[m.average_happiness] += 1
            avg_happiness = list(HappinessLevel.objects.filter(
                member__in=members_of_same_team).aggregate(Avg('happiness_level')).values())[0]
            data = {"happiness_level": happy_meter,
                    "average_happiness_of_your_team": avg_happiness}
            return Response(data, status=status.HTTP_200_OK)

    avg_happiness = list(HappinessLevel.objects.all().aggregate(Avg('happiness_level')).values())[0]
    d = {"average_happiness_across_all_teams": avg_happiness}
    return Response(d, status=status.HTTP_200_OK)


@api_view(['GET'])
def teamView(request):
    """
    One can view the teams in this endpoint with a valid token.
    """
    if 'token' not in request.query_params:
        return Response('valid token required', status=status.HTTP_400_BAD_REQUEST)
    member = Member.objects.filter(token=request.query_params['token']).first()
    if not member:
        return Response('provided token is invalid', status=status.HTTP_400_BAD_REQUEST)

    teams = Team.objects.all()
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def memberView(request):
    """
    A member can see their information by hitting
    this endpoint. Again a valid token is required.
    Again a valid token is required to view one's
    information.
    """
    if 'token' not in request.query_params:
        return Response('valid token required', status=status.HTTP_400_BAD_REQUEST)
    member = Member.objects.filter(token=request.query_params['token']).first()
    if not member:
        return Response('provided token is invalid', status=status.HTTP_400_BAD_REQUEST)
    serializer = MemberSerializer(member)
    return Response(serializer.data)