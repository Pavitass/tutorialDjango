from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..infra.factories import PaymentFactory
from ..services import CompraService
from ..models import Libro
from .serializers import LibroSerializer, OrdenInputSerializer


class CompraAPIView(APIView):
    def get(self, request):
        serializer = OrdenInputSerializer()
        return Response(
            {
                "detail": "Usa POST con libro_id y direccion_envio para comprar.",
                "fields": serializer.get_fields().keys(),
                "example": {"libro_id": 1, "direccion_envio": "Calle 123"},
            }
        )

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


class ProductosAPIView(APIView):
    def get(self, request):
        libros = Libro.objects.all().order_by("id")
        return Response(LibroSerializer(libros, many=True).data)

