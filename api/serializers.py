from rest_framework import serializers
from core.models import Actor


class ActorSerializer(serializers.ModelSerializer):
    '''Serializer for creating and deleting actors'''
    class Meta:
        model = Actor
        fields = ['id', 'name', 'vote']
        read_only_fields = ['id']


class VoteSerializer(ActorSerializer):
    '''Serializer for upvoting and downvoting an actor'''
    class Meta(ActorSerializer.Meta):
        fields = ['id', 'vote']
