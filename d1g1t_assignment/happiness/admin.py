from .models import Member, Team, HappinessLevel
from django.contrib import admin

class HappinessLevelAdmin(admin.ModelAdmin):
    model = HappinessLevel
    raw_id_fields = ('member',)


class TeamAdmin(admin.ModelAdmin):
    model = Team


class MemberAdmin(admin.ModelAdmin):
    model = Member
    raw_id_fields = ('member', 'team')


admin.site.register(HappinessLevel, HappinessLevelAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Team, TeamAdmin)