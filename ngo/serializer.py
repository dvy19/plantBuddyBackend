

from rest_framework import serializers

from .models import NGO, Campaign


class NGOSerializer(serializers.ModelSerializer):
    class Meta:
        model = NGO
        fields = "__all__"
        read_only_fields = ['created_at', 'updated_at' , 'user']
class CampaignSerializer(serializers.ModelSerializer):

    class Meta:
        model = Campaign
        fields = "__all__"
        read_only_fields = [
            "ngo",
            "current_volunteers",
            "current_amount",
            "created_at",
            "updated_at"
        ]
   
