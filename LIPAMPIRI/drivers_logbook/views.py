from rest_framework import viewsets
from .models import LogBook
from .serializers import LogBookSerializer

class LogBookViewSet(viewsets.ModelViewSet):
    queryset = LogBook.objects.all()
    serializer_class = LogBookSerializer
