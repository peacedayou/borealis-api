from rest_framework import viewsets
from .models import BorealisDataset
from .serializers import BorealisDatasetSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class BorealisDatasetViewSet(viewsets.ModelViewSet):
    queryset = BorealisDataset.objects.all()
    serializer_class = BorealisDatasetSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        results = BorealisDataset.search(request.query_params.get('q', ''))
        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data)