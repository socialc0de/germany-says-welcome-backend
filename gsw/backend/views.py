from backend.models import Question
from backend.serializers import *
from rest_framework import generics, viewsets
from django.contrib.auth.models import User
from rest_framework import permissions
from backend.permissions import IsOwnerOrReadOnly
from rest_framework import filters

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('question',)
    lookup_field = "county"
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class POIViewSet(viewsets.ModelViewSet):

    queryset = POI.objects.all()
    serializer_class = POISerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    lookup_field = "county"
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class PhraseCollectionViewSet(viewsets.ModelViewSet):

    queryset = PhraseCollection.objects.all()
    serializer_class = PhraseCollectionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class PhraseViewSet(viewsets.ModelViewSet):

    queryset = Phrase.objects.all()
    serializer_class = PhraseSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    def perform_create(self, serializer):
        serializer.save(translator=self.request.user)

class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)