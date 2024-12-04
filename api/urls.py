from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PointViewSet, MeasurementViewSet, StandardViewSet

router = DefaultRouter()
router.register(r'points', PointViewSet)
router.register(r'measurements', MeasurementViewSet)
router.register(r'standards', StandardViewSet)

urlpatterns = [
    path('', include(router.urls))
]
