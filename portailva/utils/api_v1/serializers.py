from rest_framework import serializers

from portailva.utils.models import Place


class PlaceSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Place
        fields = ('name', 'lat', 'long',)
