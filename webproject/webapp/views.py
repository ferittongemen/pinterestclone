from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .forms import AddPhotoForm, SignUpForm, UserCustimizationForm, UserProfileUpdateForm, CommentForm
from . import models
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.

@login_required(login_url="/login")
def index(request):
    pass

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(reverse("webapp:profilecustomization"))
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required(login_url="/login")
def profilecustomization(request):

    if request.method == "POST":
        form = UserCustimizationForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            post = form.save(commit=False)
            post.username = request.user
            post.save()
            return redirect(reverse('webapp:feed'))
        else:
            print(form.errors)
    else:
        form = UserCustimizationForm()
        
    return render(request, "webapp/usercustimization.html", context={"form": form})

def update_profile(request):
    user_profile = request.user.userprofile  # Kullanıcının profil örneğini al
    if request.method == "POST":
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=user_profile )
        if form.is_valid():
            form.save()
            return redirect(reverse('webapp:feed'))  # Profil sayfasına yönlendir
    else:
        form = UserProfileUpdateForm(instance=user_profile)

    return render(request, "webapp/userupdate.html", context={"form": form})    


@login_required(login_url="/login")
def addphoto(request):

    if request.method == "POST":
        # Formu oluştururken request.user'ı iletebilirsiniz
        form = AddPhotoForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            # Formu kaydetmeden önce user alanını doldur
            post = form.save(commit=False)
            post.username = request.user
            post.save()
            return redirect(reverse('webapp:feed'))
        else:
            print(form.errors)
    else:
        form = AddPhotoForm()

    return render(request, "webapp/addphoto.html", context={"form": form})

@login_required(login_url="/login")
def deletephoto(request, id):
    deleted_posts = models.WebAppModel.objects.get(pk = id)
    if request.user == deleted_posts.username:
        models.WebAppModel.objects.filter(id=id).delete()
        return redirect(reverse('webapp:feed'))
        

def feed(request):

    posts = models.WebAppModel.objects.all()
    context = {"posts":posts}
    print(posts.values)
    return render(request, "webapp/feed.html", context=context)


@login_required(login_url="/login")
def userprofile(request):
    user_posts = models.WebAppModel.objects.filter(username=request.user)
    context = {'user_posts': user_posts}
    return render(request, 'webapp/userprofile.html', context=context)

def user_selected_profile(request, id):
    user_posts = models.WebAppModel.objects.filter(username = id)
    context = {'user_posts': user_posts}
    return render(request, 'webapp/user_selected_profile.html', context=context)

def search(request):
    if request.method == 'POST':
        print(request.POST["search"])
        user_keyword = request.POST["search"]
        queryset = models.WebAppModel.objects.filter(
            Q(description = user_keyword)|
            Q(description__contains = user_keyword)|
            Q(description__icontains = user_keyword)|
            Q(description__startswith=user_keyword)|
            Q(description__endswith=user_keyword)|
            Q(description__in=[user_keyword])                              
                                                                                              )   
        
        print('--QUERYSET--',queryset.all())
        return render(request,'webapp/searchresults.html', context={'queryset':queryset})
    
def search_profile(request):

    if request.method == 'POST':
        print(request.user)
        user_keyword = request.POST["search"]
        queryset = models.WebAppModel.objects.filter(username=request.user).filter(
                Q(description = user_keyword)|
                Q(description__contains = user_keyword)|
                Q(description__icontains = user_keyword)|
                Q(description__startswith=user_keyword)|
                Q(description__endswith=user_keyword)|
                Q(description__in=[user_keyword])         
        )
        return render(request,'webapp/searchresults.html', context={'queryset':queryset})

        

    
@login_required(login_url="/login")
# views.py
def post_detail(request, post_id):
    post = get_object_or_404(models.WebAppModel, id=post_id)
    comments = post.usercomments_set.all()

    # Beğeni sayısını ve beğenen kullanıcıları al
    like_count = models.Like.like_count(post)
    likers = models.Like.objects.filter(post=post).values_list('user__username', flat=True)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            user = request.user
            models.UserComments.objects.create(comment=comment, user=user, web_app_model=post)
            return redirect('webapp:post_detail', post_id=post_id)
    else:
        form = CommentForm()
    
    return render(request, 'webapp/post_detail.html', {'post': post, 'comments': comments, 'form': form, 'like_count': like_count, 'likers': likers})


def like_post(request, post_id):
    post = get_object_or_404(models.WebAppModel, id=post_id)

    # Kontrol et: Kullanıcı daha önce beğenmiş mi?
    if models.Like.objects.filter(user=request.user, post=post).exists():
        # Kullanıcı zaten beğenmiş, isteğini geri çevir veya hata mesajı gönder
        pass
    else:
        # Kullanıcı beğenmediyse, yeni bir Like nesnesi oluştur
        models.Like.objects.create(user=request.user, post=post)

    # Beğeni sayısını hesapla
    like_count = models.Like.like_count(post)

    # post_detail URL'sini al ve like_count parametresini ekleyerek yönlendir
    post_detail_url = reverse('webapp:post_detail', kwargs={'post_id': post_id})
    post_detail_url += f'?like_count={like_count}'
    return redirect(post_detail_url)