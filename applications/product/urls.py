from django.urls import path, include
from rest_framework.routers import DefaultRouter

from applications.product.views import *

router = DefaultRouter()
router.register('', ProductViewSet)

urlpatterns = [
    # path('', ListCreateView.as_view()),
    # path('<int:pk>/', DeleteUpdateRetriveView.as_view())
    # path('', ProductViewSet.as_view({'get': 'list'})),
    # path('', ProductViewSet.as_view({'post': 'create'})),
    # path('', ProductViewSet.as_view()),
    path('category/', CategoryListCreateView.as_view()),
    path('category/<str:slug>/', CategoryRetriveDeleteUpdateView.as_view()),
    path('', include(router.urls)),         # он сам распределяет GET POST запросы весь CRUD |       нужно роутер в конце писать
]

