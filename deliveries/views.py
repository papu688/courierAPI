from datetime import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import CustomUser, Parcel, DeliveryProof
from .serializers import *
from .permissions import IsAdmin, IsCourier, IsCustomer
from rest_framework.decorators import action


class CustomUserViewset(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    


class ParcelViewset(viewsets.ModelViewSet):
    queryset = Parcel.objects.all()
    serializer_class = ParcelSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsCustomer()]
        elif self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsCourier()]
        elif self.action == 'destroy':
            return [IsAuthenticated(), IsCustomer()]
        elif self.action == 'list':
            return [IsAuthenticated(), IsAdmin()]

        return super().get_permissions()
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsCustomer])
    def confirm_delivery(self, request, pk=None):
        parcel = self.get_object()
        if request.user != parcel.sender:
            return Response({"error": "You do not have permission to confirm delivery for this parcel."}, status=status.HTTP_403_FORBIDDEN)
        if parcel.status != 'in_transit':
            return Response({"error": "Parcel status must be 'in_transit' to confirm delivery."}, status=status.HTTP_400_BAD_REQUEST)
        parcel.status = 'delivered'
        parcel.delivered_at = timezone.now()
        parcel.save()
        return Response({"status": "Delivery confirmed successfully."}, status=status.HTTP_200_OK)


class DeliveryProofViewset(viewsets.ModelViewSet):
    queryset = DeliveryProof.objects.all()
    serializer_class = DeliveryProofSerializer
    permission_classes = [IsAuthenticated, IsCourier]

    def get_permissions(self):
        #Couriers can only create or update delivery proofs for parcels they are assigned to.
        if self.action in ['create', 'update', 'partial_update']:
            return [IsAuthenticated(), IsCourier()]
        return super().get_permissions()
    
    def create(self, request,*args, **kwargs):
        parcel_id = request.data.get('parcel')
        try:
            parcel =  Parcel.objects.get(id=parcel_id)
        except Parcel.DoesNotExist:
            return Response({"error": "Parcel doesn't exist."}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user != parcel.courier:
            return Response({"error": "You are not assigned to this parcel."}, status=status.HTTP_403_FORBIDDEN)
        
        return super().create(request, *args, **kwargs)
