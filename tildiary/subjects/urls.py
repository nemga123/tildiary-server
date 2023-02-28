from django.urls import include, path
from rest_framework.routers import SimpleRouter

from subjects.views import SubjectViewSet

app_name = "subjects"

router = SimpleRouter()
router.register("", SubjectViewSet, basename="subject")

urlpatterns = [
    path("", include(router.urls)),
]
