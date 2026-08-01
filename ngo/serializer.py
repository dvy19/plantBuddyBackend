

from django.core import serializers

from core.ngo.models import NGO


class NGOSerializer(serializers.ModelSerializer):
    class Meta:
        model = NGO
        fields = "__all__"