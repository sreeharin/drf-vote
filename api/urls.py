from rest_framework.routers import DefaultRouter
from api.views import ActorViewSet, ActorsRankViewSet


router = DefaultRouter()
router.register('actors', ActorViewSet, basename='actor')
router.register('rank', ActorsRankViewSet, basename='rank')

app_name='api'
urlpatterns = router.urls