from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class PlantType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class LightRequirement(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class HomePlace(models.Model):
    name=models.CharField(max_length=20 , blank=True , null=True)

    def __str__(self):
        return self.name


class WaterRequirement(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class GrowthRate(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Lifespan(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Season(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class SoilType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Plant(models.Model):
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=150)
    description = models.TextField()

    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    plant_type = models.ForeignKey(PlantType, on_delete=models.PROTECT)
    light_requirement = models.ForeignKey(LightRequirement, on_delete=models.PROTECT)
    water_requirement = models.ForeignKey(WaterRequirement, on_delete=models.PROTECT)
    growth_rate = models.ForeignKey(GrowthRate, on_delete=models.PROTECT)
    lifespan = models.ForeignKey(Lifespan, on_delete=models.PROTECT)
    soil_type = models.ForeignKey(SoilType, on_delete=models.PROTECT)

    best_planting_season = models.ForeignKey(
        Season,
        related_name="planting_plants",
        on_delete=models.PROTECT
    )

    flowering_season = models.ForeignKey(
        Season,
        related_name="flowering_plants",
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    fruiting_season = models.ForeignKey(
        Season,
        related_name="fruiting_plants",
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    temperature_min = models.IntegerField()
    temperature_max = models.IntegerField()

    humidity = models.CharField(max_length=50)
    average_height = models.CharField(max_length=50)
    fertilizer = models.CharField(max_length=100)
    repotting_frequency = models.CharField(max_length=50)

    pruning_required = models.BooleanField(default=False)
    pet_friendly = models.BooleanField(default=False)
    air_purifying = models.BooleanField(default=False)
    edible = models.BooleanField(default=False)

    image_url = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name