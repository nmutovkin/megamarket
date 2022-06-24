from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (DeleteViewSet, ImportViewSet, NodeViewSet, SalesViewSet,
                    StatisticsViewSet)

router = DefaultRouter(trailing_slash=False)
router.register('imports', ImportViewSet)
router.register('nodes', NodeViewSet)
router.register('delete', DeleteViewSet)
router.register('sales', SalesViewSet)
router.register('node', StatisticsViewSet)

urlpatterns = [
    path('', include(router.urls))
]
