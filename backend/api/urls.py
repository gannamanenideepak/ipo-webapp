from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, IPOViewSet, AdminStatsView

router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'ipo', IPOViewSet, basename='ipo')

urlpatterns = [
    path('', include(router.urls)),
    # Optional explicit search path for IPOs
    path('ipos/search/', IPOViewSet.as_view({'get': 'list'}), name='ipo-search'),
    # Admin stats
    path('admin/stats/', AdminStatsView.as_view(), name='admin-stats'),
]
