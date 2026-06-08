from rest_framework import serializers

from .models import ConditionCategory, Condition


class ConditionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ConditionCategory
        fields = '__all__'

    def create(self, validated_data, *args, **kwargs):
        """
        Manually increment instance id
        """
        instance = self.Meta.model(**validated_data)
        instance.id = ConditionCategory.objects.latest('id').id + 1
        instance.save()
        return instance


class ConditionSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Condition
        fields = '__all__'

    def create(self, validated_data, *args, **kwargs):
        """
        Manually increment instance id
        """
        instance = self.Meta.model(**validated_data)
        instance.id = Condition.objects.latest('id').id + 1
        instance.save()
        return instance
