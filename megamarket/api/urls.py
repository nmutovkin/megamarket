from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ImportViewSet

router = DefaultRouter(trailing_slash=False)
router.register('imports', ImportViewSet)

urlpatterns = [
    path('', include(router.urls))
]
