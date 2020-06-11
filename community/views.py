from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Review
from .forms import ReviewForm
# Create your views here.
def index(request):
    reviews = Review.objects.order_by('-pk')
    context = {
        'reviews': reviews
    }
    return render(request, 'community/index.html', context)

@login_required
def create(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.save()
                return redirect('community:detail', review.pk)
        else:
            form = ReviewForm()
        context = {
            'form': form,
        }
        return render(request, 'community/form.html', context)
    else:
        return redirect('accounts:login')

def detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    context = {
        'review': review,
    }
    return render(request, 'community/review_detail.html', context)

@login_required
def update(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user==review.user:
        if request.method=='POST':
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.save()
                return redirect('community:detail', review.pk)
        else:
            form = ReviewForm(instance=review)
        context = {
            'form': form
        }
        return render(request, 'community/form.html', context)
    return redirect('community:detail', review.pk)

@login_required
def delete(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user==review.user:
        review.delete()
    else:
        return redirect('community:detail', review.pk)
    return redirect('community:index')