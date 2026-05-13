"""
URL configuration for plataforma_ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app1 import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('admin/', admin.site.urls),
    path('clientes/crear/', views.crearCliente, name='crear_cliente'),
    path('clientes/', views.listarClientes, name='listar_clientes'),
    path('pedidos/crear/', views.crearPedido, name='crear_pedido'),
    path('compra/', views.realizarCompra, name= 'realizar_compra'),
    path('pedidos/', views.listarPedidos, name='listar_pedidos'),
    path('pedidos/<int:pedido_id>/', views.detallePedido, name='detalle_pedido'),
]
