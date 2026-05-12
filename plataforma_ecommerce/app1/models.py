from django.db import models

# Create your models here.

class Client(models.Model):
    nombre = models.CharField(max_length=100)
    email= models.EmailField(unique= True)

    def __str__(self):
        return self.nombre 
    
class Pedido(models.Model):
    fecha= models.DateTimeField( auto_now_add= True)
    cliente = models.ForeignKey(Client, on_delete=models.CASCADE) 
    
    def __str__(self):
        return f"pedido #{self.id} - {self.cliente.nombre}"
    


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.CharField(max_length=100)
    cantidad = models.IntegerField()


    def __str__(self):
        return f"{self.producto}"    