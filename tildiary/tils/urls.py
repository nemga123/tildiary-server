from django.urls import include, path
from rest_framework.routers import SimpleRouter

from tils.views import *

app_name = "tils"

router = SimpleRouter()
router.register("", TilViewSet, basename="til")

urlpatterns = [
    path("", include(router.urls)),
]
