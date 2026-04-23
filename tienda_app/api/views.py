from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..infra.factories import PaymentFactory
from ..services import CompraService
from .serializers import OrdenInputSerializer


class CompraAPIView(APIView):
    def post(self, request):
        serializer = OrdenInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        procesador = PaymentFactory.get_processor()
        service = CompraService(procesador_pago=procesador)

        data = serializer.validated_data
        try:
            total = service.ejecutar_compra(
                libro_id=data["libro_id"],
                cantidad=1,
                direccion=data.get("direccion_envio", ""),
                usuario=request.user
                if getattr(request, "user", None) and request.user.is_authenticated
                else None,
            )
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"total": float(total)}, status=status.HTTP_201_CREATED)

