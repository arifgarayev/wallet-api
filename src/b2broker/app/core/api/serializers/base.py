from rest_framework import serializers


class BaseOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    modified_at = serializers.DateTimeField()

    class Meta:
        resource_name = "Wallet"
