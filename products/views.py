from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm,ProductSearchForm
from .models import Product, Hashtag
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from django.views.generic.edit import FormView
from django.db.models import Q


def products(request):
    products = Product.objects.all().order_by('pk')
    sort = request.GET.get('sort', '')
    if sort == 'mark':
        products = Product.objects.all().order_by('-mark_user', '-created_at')
    elif sort == 'recently':
        products = Product.objects.all().order_by('-created_at')
    else:
        products = Product.objects.all().order_by('pk')

    context = {
        'products': products,
        'sort': sort,
    }
    return render(request, 'products/products.html', context)


@require_POST
def mark(request, pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=pk)
        if product.mark_user.filter(pk=request.user.pk).exists():
            product.mark_user.remove(request.user)
        else:
            product.mark_user.add(request.user)
        return redirect('products:product_detail', product.pk)
    return redirect('accounts:login')


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.update_counter()
    marks = product.mark_user.count()
    hits = product.hit
    hashtags = product.hashtags.all()
    context = {
        'product': product,
        'marks': marks,
        'hits': hits,
        'hashtags':hashtags,
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
            for word in product.content.split():
                if word.startswith('#'):
                    hashtag, created = Hashtag.objects.get_or_create(tag=word)
                    product.hashtags.add(hashtag.pk)
            return redirect('products:product_detail', product.pk)
    else:
        form = ProductForm()
    context = {'form': form}
    return render(request, 'products/create.html', context)


@require_POST
def delete(request, pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Product, pk=pk)
        article.delete()
    return redirect('products:products')


@login_required
@require_http_methods(['GET', 'POST'])
def update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.seller == request.user:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                product = form.save()
                product.hashtags.clear()
                for word in product.content.split():
                    if word.startswith('#'):
                        hashtag, created = Hashtag.objects.get_or_create(tag=word)
                        product.hashtags.add(hashtag.pk)
                return redirect('products:product_detail', product.pk)
            else:
                form = ProductForm(instance=product)
    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'products/update.html', context)



class SearchFormView(FormView):
    template_name = 'products/search.html'
    form_class = ProductSearchForm

    def form_valid(self, form):
        searchWord = form.cleaned_data['search_word']
        product_list = Product.objects.filter(Q(title__icontains=searchWord) | Q(content__icontains=searchWord)).distinct()

        context = {
                'form': form,
                'search_term': searchWord,
                'product_list': product_list
            }
    
        return render(self.request, self.template_name, context)

