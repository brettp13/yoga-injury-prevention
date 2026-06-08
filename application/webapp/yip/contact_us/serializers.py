from rest_framework import serializers

from .models import ContactMessage


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'

    def create(self, validated_data, *args, **kwargs):
        """
        Manually increment instance id value
        """
        instance = self.Meta.model(**validated_data)
        instance.id = ContactMessage.objects.latest('id').id + 1
        instance.save()
        return instance