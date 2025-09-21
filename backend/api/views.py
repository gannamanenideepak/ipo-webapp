from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.http import FileResponse, Http404
from django.contrib.auth.models import User
from .models import Company, IPO
from .serializers import CompanySerializer, IPOSerializer
from .permissions import IsAdminOrReadOnly
import os

# --------------------------
# Company ViewSet
# --------------------------
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAdminOrReadOnly]
     # ✅ Added filters so frontend search & sort works
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'sector']  # frontend search box works with ?search=
    ordering_fields = ['name', 'created_at']  # can sort by name or created date

# --------------------------
# IPO ViewSet
# --------------------------
class IPOViewSet(viewsets.ModelViewSet):
    queryset = IPO.objects.select_related('company').all()
    serializer_class = IPOSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'company__id']
    search_fields = ['company__name', 'price_band', 'issue_type']
    ordering_fields = ['open_date', 'ipo_price', 'created_at']

    parser_classes = [MultiPartParser, FormParser]

    # Upload RHP/DRHP
    @action(detail=True, methods=['post'], url_path='upload', permission_classes=[permissions.IsAuthenticated])
    def upload_documents(self, request, pk=None):
        ipo = self.get_object()
        rhp = request.FILES.get('rhp_pdf')
        drhp = request.FILES.get('drhp_pdf')
        changed = False
        if rhp:
            ipo.rhp_pdf.save(rhp.name, rhp, save=False)
            changed = True
        if drhp:
            ipo.drhp_pdf.save(drhp.name, drhp, save=False)
            changed = True
        if changed:
            ipo.save()
        serializer = self.get_serializer(ipo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Download RHP/DRHP
    @action(detail=True, methods=['get'], url_path='download', permission_classes=[permissions.AllowAny])
    def download_document(self, request, pk=None):
        which = request.query_params.get('which', 'rhp')
        ipo = self.get_object()
        file_field = ipo.rhp_pdf if which == 'rhp' else ipo.drhp_pdf
        if not file_field:
            return Response({"detail": "File not found."}, status=status.HTTP_404_NOT_FOUND)
        file_path = file_field.path
        if not os.path.exists(file_path):
            raise Http404
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))

    # Delete RHP/DRHP
    @action(detail=True, methods=['post'], url_path='delete-doc', permission_classes=[permissions.IsAuthenticated])
    def delete_document(self, request, pk=None):
        which = request.query_params.get('which', 'rhp')
        ipo = self.get_object()
        if which == 'rhp' and ipo.rhp_pdf:
            ipo.rhp_pdf.delete(save=False)
            ipo.rhp_pdf = None
        elif which == 'drhp' and ipo.drhp_pdf:
            ipo.drhp_pdf.delete(save=False)
            ipo.drhp_pdf = None
        ipo.save()
        return Response({"detail": "Deleted"}, status=status.HTTP_200_OK)

# --------------------------
# Admin Stats View
# --------------------------
class AdminStatsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        total_companies = Company.objects.count()
        total_ipos = IPO.objects.count()
        total_users = User.objects.count()
        return Response({
            "total_companies": total_companies,
            "total_ipos": total_ipos,
            "total_users": total_users
        })
