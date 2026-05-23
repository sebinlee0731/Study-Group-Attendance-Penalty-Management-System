from rest_framework import serializers
from .models import Study, StudyMember, StudySchedule


class StudySerializer(serializers.ModelSerializer):
    leader_name = serializers.CharField(source='leader.username', read_only=True)

    class Meta:
        model = Study
        fields = '__all__'


class StudyMemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = StudyMember
        fields = '__all__'


class StudyScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudySchedule
        fields = '__all__'