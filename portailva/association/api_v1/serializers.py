from rest_framework import serializers

from portailva.association.models import Association


class ShortAssociationSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Association
        fields = ('id', 'name',)
