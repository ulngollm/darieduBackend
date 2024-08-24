from django.shortcuts import render
from rest_framework import viewsets

from .models import Feedback, RequestMessage
from .serializers import FeedbackSerializer, RequestMessageSerializer


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    filterset_fields = ['type']


class RequestMessageViewSet(viewsets.ModelViewSet):
    queryset = RequestMessage.objects.all()
    serializer_class = RequestMessageSerializer
    filterset_fields = ['type']
