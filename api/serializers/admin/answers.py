from rest_framework import serializers

from api import models


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Client
        fields = ('id', 'first_name', 'last_name', 'email')


class ParticipantForAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Participant
        fields = ('id', 'first_name', 'last_name', 'email', 'phone')


class BilletForAnswerSerializer(serializers.ModelSerializer):
    participants = ParticipantForAnswerSerializer(many=True, read_only=True)
    product = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.Billet
        fields = ('id', 'product', 'participants')


class OrderForAnswerSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    billets = BilletForAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = models.Order
        fields = ('id', 'client', 'status', 'billets')


class AnswerSerializer(serializers.ModelSerializer):
    billet = serializers.SlugRelatedField(slug_field='id', read_only=True)
    order = OrderForAnswerSerializer(read_only=True)

    class Meta:
        model = models.Answer
        fields = ('id', 'participant', 'question', 'value', 'order', 'billet')
