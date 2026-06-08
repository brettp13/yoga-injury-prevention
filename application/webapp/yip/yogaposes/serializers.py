from rest_framework import serializers

from .models import YogaPose, WorkAroundYogaPose


class YogaPoseSerializer(serializers.ModelSerializer):
    """
    Serialize and de-serialize yoga poses.
    """
    class Meta:
        model = YogaPose
        fields = '__all__'

    def create(self, validated_data, *args, **kwargs):
        """
        Manually increment instance id
        """
        instance = self.Meta.model(**validated_data)
        instance.id = YogaPose.objects.latest('id').id + 1
        instance.save()
        return instance


class WorkaroundSerializer(serializers.ModelSerializer):
    """
    Serialize and de-serialize workarounds
    """
    class Meta:
        model = WorkAroundYogaPose
        fields = '__all__'

    def create(self,validated_data, *args, **kwargs):
        """
        Manually increment instance id
        """
        instance = self.Meta.model(**validated_data)
        instance.id = WorkAroundYogaPose.objects.latest('id') + 1
        instance.save()
        return instance

