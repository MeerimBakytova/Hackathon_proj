from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostView, CreateCommentView, RetrieveEditDestroyCommentView

router = DefaultRouter()
router.register('', PostView)

urlpatterns = [
    path('', include(router.urls)),
    path('comment/<int:pk>/', CreateCommentView.as_view()),
    path('<int:pk>', RetrieveEditDestroyCommentView.as_view()),
]

