from django.urls import path, include
from rest_framework import routers
from .views import QuestionnaireViewSet, QuestionViewSet

router = routers.DefaultRouter()
router.register(r'questionnaire', QuestionnaireViewSet, basename='questionnaire')
router.register(r'question', QuestionViewSet, basename='question')

urlpatterns = [
    path('', include(router.urls)),
]