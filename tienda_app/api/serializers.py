from rest_framework import serializers

from ..models import Libro


class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = ("id", "titulo", "precio")


class OrdenInputSerializer(serializers.Serializer):
    libro_id = serializers.IntegerField(min_value=1)
    direccion_envio = serializers.CharField(max_length=200, allow_blank=True, default="")

