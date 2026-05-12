from django.shortcuts import render
from django.http import JsonResponse
from .models import Pedido, DetallePedido, Client
from django.db import transaction
import boto3
from datetime import datetime
# Create your views here.


def registrarEvento (userID, tipoEvento, metadatos=None):
    item = {'userID': str(userID),
            'Timestamp': datetime.utcnow().isoformat(),
            'Evento': tipoEvento,
            'Metadatos': metadatos or {},
            'IP': '127.0.0.10'}
    print (f'log de evento para dynamoDB: {item}')

def realizarCompra(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        productos = [{'nombre': 'Producto A', 'cantidad': 2}]
        try:
            with transaction.atomic():
                nuevo_pedido = Pedido.objects.create(cliente_id=cliente_id)
                for p in productos:
                    DetallePedido.objects.create(
                        producto="Producto de prueba",
                        cantidad=1,
                        pedido_id=nuevo_pedido  
                    )
                
                registrarEvento(cliente_id, "COMPRA_PRODUCTO")

            return render(request, 'exito.html', {'pedido_id': nuevo_pedido.id})

        except Exception as e:
            return render(request, 'error.html', {'mensaje': str(e)})

    return render(request, 'formulario_compra.html')
