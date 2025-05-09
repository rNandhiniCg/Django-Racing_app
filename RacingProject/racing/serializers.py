from rest_framework import serializers
from .models import Team, Driver, Race
 
class DriversTeamSerializer(serializers.ModelSerializer):
    driver_name= serializers.SerializerMethodField()
    class Meta:
        model= Driver
        fields= ['driver_name']

    def get_driver_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class TeamSerializer(serializers.ModelSerializer):
    drivers= DriversTeamSerializer( many=True, read_only=True)

    class Meta:
        model = Team
        fields = [ 'name', 'location', 'logo', 'description', 'drivers']

'''
class TeamNameSerializer(serializers.ModelSerializer):
    class Meta:
        model= Team
        fields= ['name']
''' 

class RaceShortSerializer(serializers.ModelSerializer):      #for Driver - Registered races
    race_info= serializers.SerializerMethodField()

    class Meta:
        model = Race
        fields= ['race_info']

    def get_race_info(self, obj):
        return  f"{obj.race_track_name} on {obj.race_date}"

class DriverSerializer(serializers.ModelSerializer):
    team= serializers.CharField(source='team.name')  #show only team name, not entire team info
    registered_races= RaceShortSerializer(many=True, read_only=True)
    
    class Meta:
        model = Driver
        fields = [ 'first_name', 'last_name', 'dob', 'team', 'registered_races']
        #extra_kwargs={ 'registered_races':{'required':False, 'allow_empty':True}   }
 

class SimpleDriverSerializer(serializers.ModelSerializer):   #for Race - Registered Drivers
    #team = TeamNameSerializer
    driver_name= serializers.SerializerMethodField()
    team= serializers.CharField(source='team.name')

    class Meta:
        model= Driver
        fields= ['driver_name','team']

    def get_driver_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class RaceSerializer(serializers.ModelSerializer):
    registered_drivers = SimpleDriverSerializer(many=True, read_only=True)
    
 
    class Meta:
        model = Race
        fields = ['race_track_name', 'track_location', 'race_date','registration_closure_date','registered_drivers'
        ]

#When using ModelSerializer, need to add Meta cls with model name & fields
#Here, use  'serializers.Serializer' , as taking a list of names

#Serializers - To pass driver IDs, race IDs in POST data      
class AddDriversToRaceSerializer1(serializers.Serializer):      
    drivers= serializers.PrimaryKeyRelatedField(many= True, queryset= Driver.objects.all()) 

class AddRacesToDriverSerializer1(serializers.Serializer):
    races= serializers.PrimaryKeyRelatedField(many= True, queryset= Race.objects.all())
  

#To accept names as i/p - resolve them to actual model instances
class AddDriversToRaceSerializer2(serializers.Serializer):      #Using driver names
    drivers= serializers.ListField(child= serializers.CharField())

    def validate_drivers(self, value):
        driver_objs= []
        existing_drivers= []         # already_registered
        race= self.context.get('race')     #race s/d b passed via Serializer context

        for name in value:
            try:
                first_name, last_name= name.split(' ',1)    #Assume first_name + last_name is unique
                driver= Driver.objects.get(first_name= first_name, last_name= last_name)

                if race and driver in race.registered_drivers.all():
                    existing_drivers.append(name)
                else:
                    driver_objs.append(driver)

            except(Driver.DoesNotExist, ValueError):
                raise serializers.ValidationError( f"Driver '{name}' not found or invalid format : Use 'first last'")

        if existing_drivers:
            raise serializers.ValidationError( f" Driver(s) {', '.join(existing_drivers)} already registered for the race !")
        else:
            return driver_objs
'''
#Allow only valid drivers in .save()
    def save(self, **kwargs):
        race= self.context.get('race')
        drivers= self.validated_data['drivers']
        race.drivers.add(*drivers)
        return race
'''

class AddRacesToDriverSerializer2(serializers.Serializer):  # using race names or IDs
    races = serializers.ListField(child=serializers.CharField())  # Accept race names (or IDs if you prefer) via a ListField or IntegerField() if using IDs 
 
    def validate_races(self, value):
        race_objs = []
        already_registered = []
        driver = self.context.get('driver')  # driver passed via context
 
        for race_name in value:
            try:
                race = Race.objects.get(race_track_name=race_name)  # Validate if races exist or use pk=int(race_id) if using IDs
 
                if driver and race in driver.registered_races.all():  #Check if the driver is already registered for those races
                    already_registered.append(race_name)
                else:
                    race_objs.append(race)
 
            except Race.DoesNotExist:
                raise serializers.ValidationError(f"Race '{race_name}' not found.")
 
        if already_registered:          #Raise a ValidationError if any race is already associated with the driver
            raise serializers.ValidationError(
                f"Driver already registered for races: {', '.join(already_registered)}"
            )
    
        return race_objs

    def save(self, **kwargs):                #Add only valid races in .save()
        driver = self.context.get('driver')
        races = self.validated_data['races']
        for race in races:
            race.drivers.add(driver)
        return driver

