from rest_framework import serializers

from portailva.association.api_v1.serializers import ShortAssociationSerializer
from portailva.event.models import Event, EventType, EventPrice
from portailva.utils.api_v1.serializers import PlaceSerializer


class EventTypeSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = EventType
        fields = ('name',)


class EventPriceSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta(object):
        model = EventPrice
        fields = ('id', 'name', 'price', 'is_va', 'is_variable',)

    def get_price(self, obj):
        if obj.is_variable:
            return None
        else:
            return obj.price


class EventSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    association = serializers.SerializerMethodField()
    prices = serializers.SerializerMethodField()

    class Meta(object):
        model = Event
        fields = ('name', 'short_description', 'description', 'type', 'association', 'location', 'begins_at', 'ends_at',
                  'prices',)

    def get_location(self, obj):
        return PlaceSerializer(obj.place).data

    def get_type(self, obj):
        return EventTypeSerializer(obj.type).data

    def get_association(self, obj):
        return ShortAssociationSerializer(obj.association).data

    def get_prices(self, obj):
        return EventPriceSerializer(obj.prices, many=True).data
