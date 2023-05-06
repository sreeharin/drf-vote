from rest_framework.routers import DefaultRouter
from api.views import ActorViewSet


router = DefaultRouter()
router.register('actors', ActorViewSet, basename='actor')

app_name='api'
urlpatterns = router.urls