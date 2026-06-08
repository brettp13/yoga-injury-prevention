from rest_framework import serializers

from .models import FAQ


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'

    def create(self, validated_data, *args, **kwargs):
        """
        Manually increment the id value
        """
        instance = self.Meta.model(**validated_data)
        instance.id = FAQ.objects.latest('id').id + 1
        instance.save()
        return instance