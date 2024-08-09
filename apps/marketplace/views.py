from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from utils.decorators import premium_required
from .models import MarketplaceItem
from .forms import MarketplaceItemForm, MarketplaceFilterForm

@login_required
# @premium_required
def create_item(request):
    if request.method == 'POST':
        form = MarketplaceItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.seller = request.user
            item.save()
            return redirect('marketplace:item_detail', item_id=item.id)
    else:
        form = MarketplaceItemForm()
    return render(request, 'marketplace/create_item.html', {'form': form})

@login_required
# @premium_required
def item_detail(request, item_id):
    item = get_object_or_404(MarketplaceItem, id=item_id)
    return render(request, 'marketplace/item_detail.html', {'item': item})

@login_required
# @premium_required
def item_list(request):
    items = MarketplaceItem.objects.all()
    form = MarketplaceFilterForm(request.GET)

    if form.is_valid():
        search = form.cleaned_data.get('search')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        sort_by = form.cleaned_data.get('sort_by')

        if search:
            items = items.filter(Q(title__icontains=search) | Q(description__icontains=search))
        if min_price:
            items = items.filter(price__gte=min_price)
        if max_price:
            items = items.filter(price__lte=max_price)
        if sort_by:
            items = items.order_by(sort_by)
        else:
            items = items.order_by('-created_at')

    paginator = Paginator(items, 10)  # Show 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'marketplace/item_list.html', {'items': page_obj, 'form': form})

