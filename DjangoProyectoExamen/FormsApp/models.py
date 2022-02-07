from django.db import models

from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
# Create your models here.

class Cliente(models.Model):
    idCliente = models.AutoField(max_length=5, primary_key=True)
    Nombre = models.CharField(max_length=50)
    tlf = models.CharField(max_length=10)
    def __str__(self):
        return(self.Nombre)
class Venta(models.Model):
    idVenta = models.AutoField(max_length=5, primary_key=True)
    idCliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    TotalVenta = models.FloatField(max_length=9, default=0)
    Fecha = models.DateField(auto_now_add=True)
    def __str__(self):
        return(self.idVenta)
class Producto(models.Model):
    idProducto = models.AutoField(max_length=5, primary_key=True)
    Nombre = models.CharField(max_length=50)
    PVP = models.FloatField(max_length=9)
    def __str__(self):
        return(self.Nombre)
class LineasVenta(models.Model):
    idLineaVenta = models.AutoField(max_length=5, primary_key=True)
    idVenta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    idProducto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    Cantidad = models.IntegerField(max_length=5, default=1)
    PrecioPorLinea = models.FloatField(max_length=9, default=0)
@receiver(pre_save, sender=LineasVenta)
def LineasVentaSender(sender, instance, **kwargs):
    precioporlinea = 0

    iddelproducto = instance.idProducto.idProducto

    producto = Producto.objects.get(idProducto=iddelproducto)

    precioporlinea += producto.PVP
    precioporlinea = precioporlinea * instance.Cantidad

    instance.PrecioPorLinea = precioporlinea

@receiver(post_save, sender=LineasVenta)
def AñadirPrecioVenta(sender, instance, **kwargs):
    precioporventa = 0

    iddelaventa = instance.idVenta.idVenta
    venta = Venta.objects.get(idVenta=iddelaventa)

    lineasventa = LineasVenta.objects.filter(idVenta=iddelaventa)
    for lineas in lineasventa:
        precioporventa += lineas.PrecioPorLinea
    venta.TotalVenta = precioporventa
    venta.save()
@receiver(post_delete, sender=LineasVenta)
def AñadirPrecioVenta(sender, instance, **kwargs):
    iddelaventa = instance.idVenta.idVenta
    resto = instance.PrecioPorLinea
    venta = Venta.objects.get(idVenta=iddelaventa)
    venta.TotalVenta = venta.TotalVenta - resto
    venta.save()

