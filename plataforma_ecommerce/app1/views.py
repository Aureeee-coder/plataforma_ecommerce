from django.shortcuts import render, redirect, get_object_or_404
from .models import Pedido, DetallePedido, Client
from django.db import transaction
import boto3
from datetime import datetime
# Create your views here.

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
tabla = dynamodb.Table('eventoUsuario')

def registrarEvento (userID, tipoEvento, metadatos=None):
    item = {'userID': str(userID),
            'Timestamp': datetime.utcnow().isoformat(),
            'Evento': tipoEvento,
            'IP': '127.0.0.10',
            'Metadatos': metadatos or {}
    }
    try:
        tabla.put_item(Item=item)
        print("Evento registrado en DynamoDB")
    except Exception as e:
        print(f"Error al registrar evento: {e}")

def inicio(request):
    return render(request, 'inicio.html')

def crearCliente(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')

        if not nombre or not email:
            return render(request, 'error.html', {'mensaje': 'Nombre y Email son requeridos.'})

        try:
            nuevo_cliente = Client.objects.create(nombre=nombre, email=email)
            registrarEvento(nuevo_cliente.id, "CREACION_CLIENTE")
            return redirect('listar_clientes')
        except Exception as e:
            return render(request, 'error.html', {'mensaje': str(e)})

    return render(request, 'crear_cliente.html')

def listarClientes(request):
    clientes = Client.objects.all()
    return render(request, 'listar_clientes.html', {'clientes': clientes})

def listarClientes(request):
    clientes = Client.objects.all()
    return render(request, 'listar_clientes.html', {'clientes': clientes})

def crearPedido(request):
    clientes = Client.objects.all()

    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        producto = request.POST.get('producto')
        cantidad = request.POST.get('cantidad')
        
        try:
            with transaction.atomic():
                pedido = Pedido.objects.create(cliente_id=cliente_id)

                DetallePedido.objects.create(
                            pedido=pedido.id,
                            producto=producto,
                            cantidad=cantidad,
                        )
                    
                registrarEvento(cliente_id, "CREACION_PEDIDO",{
                    'producto': producto,
                    'cantidad': cantidad
                })

            return redirect('listar_pedidos')

        except Exception as e:
                return render(request, 'error.html', {'mensaje': str(e)})
    return render(request, 'crear_pedido.html', {'clientes': clientes})

def listarPedidos(request):
    pedidos = Pedido.objects.all().order_by('-fecha_creacion')
    return render(request, 'listar_pedidos.html', {'pedidos': pedidos})

def detallePedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'detalle_pedido.html', {'pedido': pedido})

def realizarCompra(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        productos = [{'nombre': 'Producto A', 'cantidad': 2}]

        if not cliente_id:
                return render(request, 'error.html', {'mensaje': 'Cliente ID es requerido.'})

        try:
            with transaction.atomic():
                    nuevo_pedido = Pedido.objects.create(cliente_id=cliente_id)

                    for p in productos:
                        DetallePedido.objects.create(
                            producto=p['nombre'],
                            cantidad=p['cantidad'],
                            pedido_id=nuevo_pedido.id
                        )
                    
                    registrarEvento(cliente_id, "COMPRA_PRODUCTO")

                    return render(request, 'exito.html', {'pedido_id': nuevo_pedido.id})

        except Exception as e:
                return render(request, 'error.html', {'mensaje': str(e)})

    return render(request, 'formulario_compra.html')
