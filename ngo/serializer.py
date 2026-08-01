

from rest_framework import serializers

from .models import NGO


class NGOSerializer(serializers.ModelSerializer):
    class Meta:
        model = NGO
        fields = "__all__"
        read_only_fields = ['created_at', 'updated_at' , 'user']

class NgoCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = NGO
        fields = "__all__"
   
