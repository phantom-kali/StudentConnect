from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import DiningHall, MenuItem, DiningHallReview
from .forms import DiningHallReviewForm

def dining_hall_list(request):
    dining_halls = DiningHall.objects.all()
    return render(request, 'dining/dining_hall_list.html', {'dining_halls': dining_halls})

def dining_hall_detail(request, dining_hall_id):
    dining_hall = get_object_or_404(DiningHall, id=dining_hall_id)
    menu_items = dining_hall.menu_items.filter(is_available=True)
    reviews = dining_hall.reviews.order_by('-created_at')
    
    if request.method == 'POST':
        form = DiningHallReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.dining_hall = dining_hall
            review.user = request.user
            review.save()
            return redirect('dining:dining_hall_detail', dining_hall_id=dining_hall.id)
    else:
        form = DiningHallReviewForm()
    
    return render(request, 'dining/dining_hall_detail.html', {
        'dining_hall': dining_hall,
        'menu_items': menu_items,
        'reviews': reviews,
        'form': form
    })

@login_required
def update_menu_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    if request.method == 'POST':
        is_available = request.POST.get('is_available') == 'on'
        item.is_available = is_available
        item.save()
    return redirect('dining:dining_hall_detail', dining_hall_id=item.dining_hall.id)