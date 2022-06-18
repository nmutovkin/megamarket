from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DeleteViewSet, ImportViewSet, NodeViewSet

router = DefaultRouter(trailing_slash=False)
router.register('imports', ImportViewSet)
router.register('nodes', NodeViewSet)
router.register('delete', DeleteViewSet)

urlpatterns = [
    path('', include(router.urls))
]
