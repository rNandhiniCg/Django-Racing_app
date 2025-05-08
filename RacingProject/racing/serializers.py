from rest_framework import serializers
from .models import Team, Driver, Race
 
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'
        extra_kwargs={
            'drivers':{'required':False, 'allow_empty':True}
        }
 
class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'
        extra_kwargs={
            'registered_races':{'required':False, 'allow_empty':True}
        }
 
class RaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race
        fields = '__all__'