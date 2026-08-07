from django.urls import path, include
from rest_framework.routers import DefaultRouter
<<<<<<< HEAD
from .views import StudentViewSet

=======

from .views import StudentViewSet


>>>>>>> fe439967a4c9f5b0fe6a6889a838d7af247ac1c1
router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')

urlpatterns = [
    path('', include(router.urls)),
]