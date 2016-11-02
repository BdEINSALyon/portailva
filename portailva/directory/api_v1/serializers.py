from rest_framework import serializers

from portailva.directory.models import OpeningHour, DirectoryEntry
from portailva.utils.api_v1.serializers import PlaceSerializer


class OpeningHourSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = OpeningHour
        fields = ('day', 'begins_at', 'ends_at',)


class DirectoryEntrySerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    opening_hours = serializers.SerializerMethodField()

    class Meta(object):
        model = DirectoryEntry
        fields = ('id', 'name', 'short_description', 'description', 'contact_address', 'phone', 'website_url',
                  'facebook_url', 'twitter_url', 'location', 'opening_hours',)

    def get_id(self, obj):
        return obj.association_id

    def get_name(self, obj):
        return obj.association.name

    def get_short_description(self, obj):
        if len(obj.description) > 150:
            return obj.description[:150] + "..."
        else:
            return obj.description

    def get_location(self, obj):
        return PlaceSerializer(obj.place).data

    def get_opening_hours(self, obj):
        return OpeningHourSerializer(obj.opening_hours.all(), many=True).data
