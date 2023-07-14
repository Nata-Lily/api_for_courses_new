import uuid

from .models import Course, Participant, User
from django.conf import settings
from django.core.exceptions import PermissionDenied

from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import AdminPermission, IsModeratorOrReadOnly
from .serializers import (
    CourseSerializer,
    ParticipantSerializer,
    SignUpSerializer,
    TokenSerializer,
    UserSerializer
)

BAD_CODE = '0'
DATE_FORMAT = '%Y-%m-%d'


def send_confirmation_code_and_save(username):
    user = get_object_or_404(User, username=username)
    user.confirmation_code = str(uuid.uuid4())
    send_mail(
        'Ваш код подтверждения',
        f'Код для получения JWT токена {user.confirmation_code}',
        settings.EMAIL_FOR_AUTH_LETTERS,
        [user.email],
        fail_silently=False,
    )
    user.save()


@api_view(['POST'])
@permission_classes([AllowAny])
def registration(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')
    try:
        user, _ = User.objects.get_or_create(
            email=email,
            username=username
        )
    except IntegrityError:
        return Response(
            f'Такой {username} или {email} уже существуют',
            status=status.HTTP_400_BAD_REQUEST
        )
    send_confirmation_code_and_save(username)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if (
        user.confirmation_code != confirmation_code
        or user.confirmation_code == BAD_CODE
    ):
        result = Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        result = Response(
            {"token": str(RefreshToken.for_user(user).access_token)},
            status=status.HTTP_200_OK
        )
    user.confirmation_code = BAD_CODE
    user.save()
    return result


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminPermission,)
    search_fields = ('username',)
    lookup_field = 'username'


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsModeratorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'start_date', 'description')

    def perform_create(self, serializer):
        if not self.request.user.is_moderator:
            raise PermissionDenied()
        return serializer.save()


class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
