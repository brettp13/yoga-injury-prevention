from rest_framework import serializers

from .models import AcknowledgedGroup, AcknowledgedPerson


class AcknowledgedGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcknowledgedGroup
        fields = '__all__'

    def create(self, validated_data, *args, **kwargs):
        """
        Manually increment instance id
        """
        instance = self.Meta.model(**validated_data)
        instance.id = AcknowledgedGroup.objects.latest('id').id + 1
        instance.save()
        return instance


class AcknowledgedPersonSerializer(serializers.ModelSerializer):
    group = serializers.ReadOnlyField(source='group.title')

    class Meta:
        model = AcknowledgedPerson
        fields = '__all__'

    def create(self, validated_data, *args, **kwargs):
        """
        Manually increment instance id value
        """
        instance = self.Meta.model(**validated_data)
        instance.id = AcknowledgedPerson.objects.latest('id').id + 1
        instance.save()
        return instance
