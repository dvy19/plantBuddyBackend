from rest_framework import serializers

from plants.models import Category, PlantType, LightRequirement, WaterRequirement, SoilType, Season, Lifespan, GrowthRate, Plant , HomePlace

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class PlantTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantType
        fields = "__all__"


class LightRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = LightRequirement
        fields = "__all__"


class WaterRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterRequirement
        fields = "__all__"


class GrowthRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrowthRate
        fields = "__all__"


class LifespanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lifespan
        fields = "__all__"

class HomePlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model=HomePlace
        feilds="__all__"


class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = "__all__"


class SoilTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoilType
        fields = "__all__"

class PlantSerializer(serializers.ModelSerializer):

    category = CategorySerializer(read_only=True)
    plant_type = PlantTypeSerializer(read_only=True)
    light_requirement = LightRequirementSerializer(read_only=True)
    water_requirement = WaterRequirementSerializer(read_only=True)
    growth_rate = GrowthRateSerializer(read_only=True)
    lifespan = LifespanSerializer(read_only=True)
    soil_type = SoilTypeSerializer(read_only=True)

    home_place=HomePlaceSerializer(read_only=True)

    best_planting_season = SeasonSerializer(read_only=True)
    flowering_season = SeasonSerializer(read_only=True)
    fruiting_season = SeasonSerializer(read_only=True)

    class Meta:
        model = Plant
        fields = "__all__"


