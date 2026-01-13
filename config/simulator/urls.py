from django.urls import path
from .views import health, fighters, simulate

urlpatterns = [
    path("health/", health),
    path("fighters/", fighters),
    path("simulate/", simulate),
]
