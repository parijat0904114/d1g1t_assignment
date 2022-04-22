from rest_framework import serializers
from .models import HappinessLevel, Team, Member


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class MemberSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.name

    class Meta:
        model = Member
        fields = '__all__'


class HappinessLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HappinessLevel
        fields = ['member', 'happiness_level', 'date']