from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
# Create your views here.

def products(request):
    products = Product.objects.all().order_by('-pk')
    context = {
        'products' : products,
    }
    return render(request, 'products/products.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product':product,
    }
    return render(request, 'products/product_detail.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('products:product_detail', product.pk)
    else:
        form = ProductForm()
    context = {'form':form}
    return render(request, 'products/create.html', context)

@require_POST
def delete(request, pk):
    if request.user.is_authenticated:
        article =get_object_or_404(Product, pk=pk)
        article.delete()
    return redirect('products:products')


@login_required
@require_http_methods(['GET','POST'])
def update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.seller == request.user:
        if request.method =='POST':
            form = ProductForm(request.POST, instance=product)
            if form.is_valid():
                product = form.save()
                return redirect('products:product_detail', product.pk)
        else:
            form = ProductForm(instance=product)
    context = {
        'form':form,
        'product':product
        }
    return render(request, 'products/update.html', context)