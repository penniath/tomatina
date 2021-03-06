from django.contrib.auth.models import Group
from rest_framework import viewsets
from api.models import Pomodoro
from django.utils import timezone
from django.contrib.auth import get_user_model
from api.helpers import get_status
from rest_framework import status
from django.conf import settings
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from api.serializers import (
    UserSerializer,
    GroupSerializer,
    UserStatusSerializer,
    ListUsersSerializer,
    PomodoroSerializer
)

User = get_user_model()


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_fields = ('username',)

    def perform_create(self, serializer):
        serializer.save()
        user_group_name = "Team %s" % serializer.instance.username
        group, error = Group.objects.get_or_create(name=user_group_name)
        serializer.instance.groups.add(group.pk)


class PomodoroViewSet(viewsets.ModelViewSet):
    queryset = Pomodoro.objects.all()
    serializer_class = PomodoroSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        pomodoros = Pomodoro.objects.filter(
            started__gte=timezone.now() - timezone.timedelta(
                seconds=settings.POMODORO_DURATION
            ),
            user_id=self.request.data['user_id'],
            is_canceled=False)

        if pomodoros:
            pomodoro = pomodoros.first()
            return PomodoroSerializer(pomodoro, context={'request': self.request})

        serializer.save(user=User.objects.get(pk=self.request.data['user_id']))
        return serializer


class UserStatusViewSet(viewsets.ModelViewSet):
    queryset = Pomodoro.objects.none()
    serializer_class = Serializer

    def list(self, request, *args, **kwargs):
        response = {'data': []}
        if 'user_id' in request.query_params:
            now = timezone.now()
            pomodoros = Pomodoro.objects.filter(
                user_id=request.query_params['user_id'][0],
                started__gte=timezone.datetime(month=now.month, year=now.year, day=now.day)
            ).order_by('-started')
            if pomodoros:
                pomodoro = pomodoros.first()
                response = {
                    'data': [{
                        'user_id': pomodoro.pk,
                        'status': get_status([k for k in pomodoros]),
                        'username': pomodoro.user.username,
                        'started': pomodoro.started,
                        'pomodoros': pomodoros.count()
                    }]
                }

        return Response(response)


class TeamStatusViewSet(viewsets.ModelViewSet):
    queryset = Pomodoro.objects.all()
    serializer_class = Serializer

    def list(self, request, *args, **kwargs):
        response = {'data': []}
        if 'group_id' in request.query_params:
            ids = list(
                User.objects.filter(groups__pk=request.query_params['group_id'][0]).values_list('pk', flat=True))
            now = timezone.now()
            pomodoros = Pomodoro.objects.filter(
                user_id__in=ids,
                started__gte=timezone.datetime(month=now.month, year=now.year, day=now.day)
            ).order_by('user_id', '-started')
            users = {}
            if pomodoros:
                for pomodoro in pomodoros:
                    if not pomodoro.user_id in users:
                        users[pomodoro.user_id] = [pomodoro]
                        continue

                    users[pomodoro.user_id].append(pomodoro)

                for user in users:
                    response['data'].append({
                        'user_id': users[user][0].pk,
                        'status': get_status(users[user]),
                        'username': pomodoro.user.username,
                        'started': users[user][0].started,
                        'pomodoros': len(users[user])
                    })

        return Response(response)
