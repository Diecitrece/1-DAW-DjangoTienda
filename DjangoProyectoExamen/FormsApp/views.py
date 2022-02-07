from django.http import HttpResponse
import datetime
from django.template import Template, Context, loader
from django.template.loader import get_template
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
# Create your views here.

def mainpage(request):
    return render(request, "main.html")

def articulos_mostrar(request):
    productos = Producto.objects.all().order_by('Nombre')
    lista_productos = list()
    for producto in productos:
        lista_productos.append(producto)
    return render(request, "articulos/articulos_mostrar.html", {'productos':lista_productos,})
def articulos_destacados(request):
    lineas = LineasVenta.objects.all()
    productos = Producto.objects.all()
    dictProductos = dict()
    listaProductos = list()
    listaDef = list()
    listaDefDef = list()
    listadoFinal = list()
    for producto in productos:
        dictProductos[producto.idProducto] = 0;
    for linea in lineas:
        for producto in productos:
            if linea.idProducto == producto:
                dictProductos[producto.idProducto] = dictProductos[producto.idProducto] + linea.Cantidad
    for producto in dictProductos:
        listaProductos.append(dictProductos[producto])
    listaProductos.sort(reverse=True)
    for producto in listaProductos:
        for key in dictProductos:
            if dictProductos[key] == producto:
                listaDef.append(key)
    for key in listaDef:
        if (key not in listaDefDef):
            listaDefDef.append(key)
    for key in listaDefDef:
        producto = Producto.objects.get(idProducto = key)
        listadoFinal.append(producto)
    listadoFinal = listadoFinal[0:3]
    print(listadoFinal)
    return render(request, "articulos/articulos_destacados.html" , {'productos' : listadoFinal})
def articulos_borrar(request, id):
    producto = Producto.objects.get(idProducto=id)
    producto.delete()
    return redirect('/articulos/')
def articulos_cambiar(request, id):
    producto = get_object_or_404(Producto, idProducto=id)
    if request.method == "POST":
        form = New_Producto(request.POST, instance=producto)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.save()
            return redirect('/articulos/', id=producto.idProducto)
    else:
        form = New_Producto(instance=producto)
    return render(request, 'articulos/articulos_form.html', {'form': form})
def articulos_crear(request):
    if request.method == "POST":
        form = New_Producto(request.POST)
        if form.is_valid():
            new_producto = form.save(commit=False)
            new_producto.save()
            return redirect('/articulos')
    else:
        form = New_Producto()
    return render(request, "articulos/articulos_form.html", {'form': form})

def clientes_mostrar(request):
    clientes = Cliente.objects.all().order_by('Nombre')
    lista_clientes = list()
    lista_facturacioncliente = list()
    ventas = Venta.objects.all()
    listado = ""
    for cliente in clientes:
        sumatorio = 0
        lista_clientes.append(cliente)
        for venta in ventas:
            if venta.idCliente == cliente:
                sumatorio = sumatorio + venta.TotalVenta
        lista_facturacioncliente.append(sumatorio)
        listado = zip(lista_clientes, lista_facturacioncliente)
    return render(request, "clientes/clientes_mostrar.html", {'listado' : listado})
def clientes_borrar(request, id):
    cliente = Cliente.objects.get(idCliente=id)
    cliente.delete()
    return redirect('/clientes/')
def clientes_cambiar(request, id):
    cliente = get_object_or_404(Cliente, idCliente=id)
    if request.method == "POST":
        form = New_Cliente(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.save()
            return redirect('/clientes/', id=cliente.idCliente)
    else:
        form = New_Cliente(instance=cliente)
    return render(request, 'clientes/clientes_form.html', {'form': form})
def clientes_crear(request):
    if request.method == "POST":
        form = New_Cliente(request.POST)
        if form.is_valid():
            new_cliente = form.save(commit=False)
            new_cliente.save()
            return redirect('/clientes')
    else:
        form = New_Cliente()
    return render(request, "clientes/clientes_form.html", {'form': form})

def ventas_mostrar(request):
    ventas = Venta.objects.all().order_by('Fecha')
    lista_ventas = list()
    lista_clientesXventa = list()
    for venta in ventas:
        lista_ventas.append(venta)
        cliente = Cliente.objects.get(idCliente=venta.idCliente.idCliente)
        lista_clientesXventa.append(cliente)
    return render(request, "ventas/ventas_mostrar.html", {'ventas': lista_ventas, 'clienteXventa': lista_clientesXventa})
def ventas_borrar(request, id):
    venta = Venta.objects.get(idVenta=id)
    venta.delete()
    return redirect('/ventas/')
def ventas_cambiar(request, id):
    venta = get_object_or_404(Venta, idVenta=id)
    if request.method == "POST":
        form = New_Venta(request.POST, instance=venta)
        if form.is_valid():
            venta = form.save(commit=False)
            venta.save()
            return redirect('/ventas/', id=venta.idVenta)
    else:
        form = New_Venta(instance=venta)
    return render(request, 'ventas/ventas_form.html', {'form': form})
def ventas_crear(request):
    if request.method == "POST":
        form = New_Venta(request.POST)
        if form.is_valid():
            new_venta = form.save(commit=False)
            new_venta.save()
            return redirect('/ventas')
    else:
        form = New_Venta()
    return render(request, "ventas/ventas_form.html", {'form': form})
def lineasventas(request, id):
    lineasventas = LineasVenta.objects.filter(idVenta=id)
    listalineasventa = list()
    lista_productosXlinea = list()
    for linea in lineasventas:
        listalineasventa.append(linea)
        producto = Producto.objects.get(idProducto = linea.idProducto.idProducto)
        lista_productosXlinea.append(producto)
    return render(request, "ventas/ventas_lineasventa.html", {'lineasventas' : listalineasventa, 'productos' : lista_productosXlinea, 'idventa' : id})
def lineasventas_crear(request, id):
    if request.method == "POST":
        form = New_LineaVenta(request.POST)
        producto_actual = Producto.objects.get(idProducto=(request.POST["idProducto"]))
        venta_actual = Venta.objects.get(idVenta = id)
        if form.is_valid():
            #aquí vemos si se está añadiendo el mismo producto de nuevo
            semaforo = 1
            lineas_venta = LineasVenta.objects.filter(idVenta = venta_actual)
            for linea in lineas_venta:
                if linea.idProducto == producto_actual:
                    linea.Cantidad = int(linea.Cantidad) + int(request.POST["Cantidad"])
                    linea.save()
                    semaforo = 0;
                    break;
                else:
                    semaforo = 1;
            if semaforo == 1:
                new_linea = form.save(commit=False)
                new_linea.save()
            return redirect('/ventas/lineasventas/' + str(id))
    else:
        venta = Venta.objects.get(idVenta=id)
        form = New_LineaVenta(initial={'idVenta' : venta})
    return render(request, "ventas/lineasventa_form.html", {'form': form})
def lineasventas_borrar(request, id, idventa):
    lineaventa = LineasVenta.objects.get(idLineaVenta=id)
    lineaventa.delete()
    return redirect('/ventas/lineasventas/' + str(idventa))

def lineasventas_cambiar(request, id, idventa):
    linea_venta = get_object_or_404(LineasVenta, idLineaVenta=id)
    venta_actual = Venta.objects.get(idVenta = idventa)
    producto_actual = linea_venta.idProducto
    if request.method == "POST":
        form = New_LineaVenta(request.POST, instance=linea_venta)
        producto_actual = Producto.objects.get(idProducto= request.POST['idProducto'])
        if form.is_valid():
            # aquí vemos si se está añadiendo el mismo producto de nuevo
            semaforo = 1
            lineas_venta = LineasVenta.objects.filter(idVenta=venta_actual)
            for linea in lineas_venta:
                if (linea.idProducto == producto_actual) and (linea.idLineaVenta != linea_venta.idLineaVenta):
                    linea.Cantidad = int(linea.Cantidad) + int(request.POST["Cantidad"])
                    linea.save()
                    linea_venta.delete()
                    semaforo = 0;
                    print("a")
                    break;

                else:
                    semaforo = 1;
            if semaforo == 1:
                linea_venta = form.save(commit=False)
                linea_venta.save()
            return redirect('/ventas/lineasventas/' + str(idventa))
    else:
        form = New_LineaVenta(initial={'idVenta' : venta_actual, 'idProducto' : producto_actual, "Cantidad" : linea_venta.Cantidad})
    return render(request, 'ventas/lineasventa_form.html', {'form': form})


