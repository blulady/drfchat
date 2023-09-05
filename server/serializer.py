from rest_framework import serializers
from .models import Category, Server, Channel


class ChannelSerializer(serializers.ModelSerializer):
    # because we want to return data from the channel model in the attribute channel_server in the next serialzier class, we need to create a serializer
    class Meta:
        model = Channel
        fields = "__all__"


class ServerSerializer(serializers.ModelSerializer):
    """the SerializerMethodField is used to write custom methods to generate a field
    value that is not derived from the model attributes"""

    num_members = serializers.SerializerMethodField()

    """whenever you return server data you will also return the channel data associated
    with that server -we can do this through the foreign key for the server on the Channel model"""
    channel_server = ChannelSerializer(many=True)

    class Meta:
        model = Server
        exclude = ["member"]

    def get_num_members(self, obj):
        """custom method to return the number of members in the server,
        telling django that num_members is connected to the queryset from
        the viewset self.queryset.annotate(num_members=Count("member"))"""
        if hasattr(obj, "num_members"):
            return obj.num_members
        return None

    def to_representation(self, instance):
        """This function will remove the num_members field from the server representation.
        if it is null and include it if not"""
        data = super().to_representation(instance)
        num_members = self.context.get("num_members")
        if not num_members:
            data.pop("num_members", None)
        return data
