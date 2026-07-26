from rest_framework import serializers

from plants.models import Category, PlantType, LightRequirement, WaterRequirement, SoilType, Season, Lifespan, GrowthRate, Plant

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        feilds='_all_'


class PlantTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=PlantType
        feilds='_all_'

class LightRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model=LightRequirement
        feilds='_all_'

class WaterRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model=WaterRequirement
        feilds='_all_'

class GrowthRateSerializer(serializers.ModelSerializer):
    class Meta:
        model=GrowthRate
        feilds='_all_'

class LifespanSerializer(serializers.ModelSerializer):
    class Meta:
        model=Lifespan
        feilds='_all_'

class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model=Season
        feilds='_all_'

class SoilTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=SoilType
        feilds='_all_'


class PlantSerializer(serializers.ModelSerializer):

    category = CategorySerializer(read_only=True)
    plant_type = PlantTypeSerializer(read_only=True)
    light_requirement = LightRequirementSerializer(read_only=True)
    water_requirement = WaterRequirementSerializer(read_only=True)
    growth_rate = GrowthRateSerializer(read_only=True)
    lifespan = LifespanSerializer(read_only=True)
    soil_type = SoilTypeSerializer(read_only=True)

    best_planting_season = SeasonSerializer(read_only=True)
    flowering_season = SeasonSerializer(read_only=True)
    fruiting_season = SeasonSerializer(read_only=True)

    class Meta:
        model = Plant
        fields = "__all__"


