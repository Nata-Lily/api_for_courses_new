from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (UsersViewSet, get_token,
                    registration, CourseViewSet, ParticipantViewSet)

app_name = 'api'

router = SimpleRouter()

router.register('users', UsersViewSet, basename='users')
router.register('course', CourseViewSet, basename='course')
router.register('participant', ParticipantViewSet, basename='participant'),

authpatterns = [
    path('signup/', registration, name='registration'),
    path('token/', get_token, name='get_token'),
]


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include(authpatterns)),
]
