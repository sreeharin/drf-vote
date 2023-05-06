from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from core.models import Actor
from api.serializers import ActorSerializer, VoteSerializer


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        '''
        Permission for creating and destroying is reserved for superuser
        '''
        if self.action == 'create' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


    @action(methods=['PATCH'], detail=True, url_path='upvote')
    def upvote(self, request, pk=None):
        '''Custom action for upvoting actor'''
        actor = self.get_object()
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid():
            actor.upvote()
            actor.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(
                data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

    @action(methods=['PATCH'], detail=True, url_path='downvote')
    def downvote(self, request, pk=None):
        '''Custom action for downvoting actor'''
        actor = self.get_object()
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid():
            actor.downvote()
            actor.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(
                data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

class ActorsRankViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    '''Viewset for viewing the actors based on their votes'''
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

    def get_queryset(self):
        return self.queryset.order_by('-vote')