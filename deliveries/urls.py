from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'users', CustomUserViewset)
router.register(r'parcels', ParcelViewset)
router.register(r'delivery_proofs', DeliveryProofViewset)


urlpatterns = [
    path('api/', include(router.urls)),
]