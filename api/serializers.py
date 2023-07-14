from .models import Course, Participant, User
from rest_framework import serializers

MAX_LENTH_USERNAME = 150
MAX_LENTH_CONFIRMATION_CODE = 120
MAX_LENTH_EMAIL = 254
CHARACTER_LIMIT = 100
BAD_CODE = '0'


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=MAX_LENTH_EMAIL,
        allow_blank=False
    )
    username = serializers.CharField(
        max_length=MAX_LENTH_USERNAME,
        allow_blank=False
    )


class TokenSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(
        max_length=MAX_LENTH_CONFIRMATION_CODE
    )
    username = serializers.CharField(
        max_length=MAX_LENTH_USERNAME,
    )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Course


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (['course_name'])
        model = Participant
