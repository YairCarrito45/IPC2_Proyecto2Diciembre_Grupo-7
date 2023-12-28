import os
from django.shortcuts import render, redirect
from .models import Cliente, Producto
from .forms import AddClienteForm, EditarClienteForm, AddProductoForm, EditProductoForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Factura, DetalleFactura
from django.db import transaction
import matplotlib
from django.db.models import Sum


# Selecciona el backend adecuado para Matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import numpy as np
from django.http import HttpResponse

# Create your views here.

def ventas_view(request):
    num_ventas = 156
    context = {
        'num_ventas': num_ventas
    }
    return render(request, 'ventas.html', context)

def clientes_view(request):
    clientes = Cliente.objects.all()
    form_personal = AddClienteForm()
    form_editar = EditarClienteForm()

    context = {
        'clientes': clientes,
        'form_personal': form_personal,
        'form_editar': form_editar
    }
    return render(request, 'clientes.html', context)

#agregar cliente desde form
def add_cliente_view(request): 
    #print("Guardar cliente")
    if request.POST:
        form = AddClienteForm(request.POST, request.FILES)
        if form.is_valid:
            try:
                form.save()
            except:
                messages(request, "Error al Guardar")
                return redirect('Clientes')


    return redirect('Clientes')

#editar formulario
def edit_cliente_view(request): 
    if request.POST:
        cliente = Cliente.objects.get(pk=request.POST.get('id_personal_editar'))
        form = EditarClienteForm(
            request.POST, request.FILES, instance= cliente)
        if form.is_valid:
            form.save()
    return redirect('Clientes')


#eliminar cliente de formulario
def delete_cliente_view(request):
    if request.POST:
        cliente = Cliente.objects.get(pk=request.POST.get('id_personal_eliminar'))
        cliente.delete()
        
    return redirect('Clientes')

def productos_view(request):
    """
    clientes = Cliente.objects.all()
    form_personal = AddClienteForm()
    form_editar = EditarClienteForm()
     """
    productos = Producto.objects.all()
    form_add = AddProductoForm()
    form_editar_producto = EditProductoForm()

    context = {
        'productos': productos,
        'form_add': form_add,
        'form_editar_producto': form_editar_producto
        
    }
    return render(request, 'productos.html', context)


#agregar producto desde form
def add_producto_view(request): 
    #print("Guardar Producto")
    if request.POST:
        form = AddProductoForm(request.POST, request.FILES)
        if form.is_valid:
            try:
                form.save()
            except:
                messages(request, "Error al Guardar el Producto")
                return redirect('Productos')
        return redirect('Productos')
    
#editar formulario
def edit_producto_view(request): 
    if request.POST:
        producto = Producto.objects.get(pk=request.POST.get('id_producto_editar'))
        form = EditProductoForm(
            request.POST, request.FILES, instance= producto)
        if form.is_valid:
            form.save()
    return redirect('Productos')

def delete_producto_view(request):
    if request.POST:
        producto = Producto.objects.get(pk=request.POST.get('id_producto_eliminar'))
        if producto.imagen:
            # Eliminar la imagen asociada al producto si existe
            if os.path.exists(producto.imagen.path):
                os.remove(producto.imagen.path)
        # Eliminar el producto
        producto.delete() 

    return redirect('Productos')

def seleccionar_cliente_view(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        
        request.session['cliente_id'] = cliente_id
    return redirect('Productos') 


@transaction.atomic
def realizar_compra_view(request):
    if request.method == 'POST':
        cliente_id = request.session.get('cliente_id')
        
        if cliente_id is None:
            messages.error(request, "Cliente no seleccionado.")
            return redirect('Clientes')

        productos_ids = request.POST.getlist('productos[]')

        try:
            with transaction.atomic():
                factura = Factura.objects.create(cliente_id=cliente_id)

                total_factura = 0
                for producto_id in productos_ids:
                    producto = Producto.objects.get(pk=producto_id)
                    if producto.stock > 0:
                        producto.stock -= 1
                        producto.save()

                        detalle = DetalleFactura.objects.create(
                            factura=factura,
                            producto=producto,
                            cantidad=1,
                            precio_unitario=producto.precio,
                            subtotal=producto.precio
                        )

                        total_factura += detalle.subtotal

                factura.total = total_factura
                factura.save()

                messages.success(request, "Compra realizada con éxito.")

        except Exception as e:
            messages.error(request, f"Error al realizar la compra: {str(e)}")

    return redirect('Productos')


def ventas_view(request):
    facturas = Factura.objects.all()
    return render(request, 'ventas.html', {'facturas': facturas})


def detalle_factura_view(request, factura_id):
    factura = get_object_or_404(Factura, pk=factura_id)
    detalles_factura = DetalleFactura.objects.filter(factura=factura)

    context = {
        'factura': factura,
        'detalles_factura': detalles_factura,
    }

    return render(request, 'detalle_factura.html', context)


def eliminar_factura_view(request, factura_id):
    factura = get_object_or_404(Factura, pk=factura_id)

    factura.delete()
    return redirect('Ventas')


def graficos_view(request):
    productos_mas_vendidos = Producto.objects.annotate(total_vendido=Sum('detallefactura__cantidad')).order_by('-total_vendido')[:10]

    productos_mas_vendidos = [p for p in productos_mas_vendidos if p.total_vendido is not None]

    nombres_productos = [p.nombre for p in productos_mas_vendidos]
    cantidades_vendidas = [p.total_vendido for p in productos_mas_vendidos]

    plt.figure(figsize=(10, 6))
    plt.bar(nombres_productos, cantidades_vendidas)
    plt.title('Productos más vendidos')
    plt.xlabel('Productos')
    plt.ylabel('Cantidad vendida')
    
    image_stream = BytesIO()
    plt.savefig(image_stream, format="png")
    plt.close()
    image_stream.seek(0)

    response = HttpResponse(content_type="image/png")
    response.write(image_stream.getvalue())
    return response

