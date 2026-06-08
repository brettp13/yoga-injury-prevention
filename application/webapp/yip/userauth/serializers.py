from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator


class UserAuthSerializer(serializers.ModelSerializer):
    """
    This class serializes and deserializes user auth objects,
    and associates a Token Authentication object with the user
    account.
    """
    username = serializers.SerializerMethodField()
    email = serializers.EmailField(required=True, max_length=254, allow_blank=False,
                                   validators=[UniqueValidator(queryset=User.objects.all())])
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'id', 'token', 'is_active', 'date_joined')
        write_only_fields = ('password',)
        read_only_fields = ('is_staff', 'is_superuser', 'is_active', 'date_joined', 'user_type')

    def get_username(self, obj):
        """
        Set username to user's email
        """
        username = obj.email
        return username

    def get_token(self, obj):
        """
        Get authentication token associated with user to return to client
        """
        email = obj.email
        user = User.objects.get(email=email)
        token = Token.objects.get(user=user)
        return token.key

    def create(self, validated_data, *args, **kwargs):
        """
        Create and return a new user instance, given the validated data
        """
        password = validated_data.pop('password', None)
        email = validated_data.pop('email', None)

        instance = self.Meta.model(**validated_data)
        instance.id = User.objects.latest('id').id + 1
        
        if password is not None:
            instance.set_password(password)
        if email is not None:
            instance.username = email.lower()
            instance.email = email.lower()
        instance.save()
        return instance

    def update(self, instance, validated_data):
        """
        Update user auth object
        """
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('email', instance.username)
        
        password = validated_data.get('password', instance.password)
        instance.set_password(password)

        instance.email = instance.email.lower()
        instance.username = instance.username.lower()

        instance.save()
        return instance


class AuthTokenViewSerializer(serializers.Serializer):
    """
    Override django-rest-framework's default AuthTokenSerializer to accept
    authentication using email password combination rather than username
    password
    """
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email').lower()
        password = data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data

