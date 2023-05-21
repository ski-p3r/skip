from contact.models import Address, SocialNetwork
from settings.models import Profile
from django.shortcuts import get_object_or_404, render
from post.models import Post
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from accounts.models import Account
from django.http import HttpResponse

@login_required(login_url = 'login')
def home(request):
    post = Post.objects.all()
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
        context = {
            'post': post,
            'profile': profile,
        }
    except:
        context = {
            'post': post,
        }
    return render(request, 'index.html', context)

@login_required(login_url = 'login')
def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            post = Post.objects.order_by('-created_date').filter(text__icontains=keyword)
    profile = Profile.objects.get(user=request.user)
    context = {
        'profile': profile,
        'post': post,
    }
    return render(request, 'index.html', context)

@login_required(login_url = 'login')
def author(request):
    username = Account.objects.get(username="manmuba80")
    if username:
        # username = get_object_or_404(Account, username=username)
        post = Post.objects.filter(user=username)
        post_count = post.count()
        profiles = Profile.objects.get(user=username)
        profile = Profile.objects.get(user=request.user)
        address = Address.objects.get(user=username)
        social = SocialNetwork.objects.get(user=username)
    context = {
        'username': username,
        'profile': profile,
        'address': address,
        'social': social,
        'profiles': profiles,
        'post': post,
        'post_count': post_count,
    }
    return render(request, 'accounts/author_admin.html', context)
    # return HttpResponse(username.email)