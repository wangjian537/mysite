import datetime
from django.shortcuts import render, redirect
from read_statistics.utils import get_seven_days_data, get_today_hot_data, get_yesterday_hot_data
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from django.contrib import auth
from blog.models import Blog
from django.core.cache import cache
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import LoginForm, RegForm

def get_seven_hot_blogs():
    today = timezone.now().date()
    seven_days = today - datetime.timedelta(days=7)
    blogs = Blog.objects.filter(read_details__date__lt=today, read_details__date__gte=seven_days).values('id', 'title').annotate(read_num_sum=Sum('read_details__read_num')).order_by('-read_num_sum')
    return blogs[:7]

def home(request):
    context = {}
    blog_content_type = ContentType.objects.get_for_model(Blog)
    read_nums, dates = get_seven_days_data(blog_content_type)

#   获取7天热门博客的缓存数据
    hot_blogs_for_7_days = cache.get('hot_blogs_for_7_days')
    if hot_blogs_for_7_days is None:
        hot_blogs_for_7_days = get_seven_hot_blogs()
        cache.set('hot_blogs_for_7_days', hot_blogs_for_7_days, 3600)

    context['read_nums'] = read_nums
    context['today_hot_data'] = get_today_hot_data(blog_content_type)
    context['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)
    context['seven_hot_blogs'] = hot_blogs_for_7_days
    context['dates'] = dates
    return render(request, 'home.html', context)

def login(request):
    """
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(request, username=username, password=password)
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    if user is not None:
        auth.login(request, user)
        return redirect(referer)
    else:
        return render(request, 'error.html', {'message': '用户名或密码不正确'})
    :param request:
    :return:
    """
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        # 判断请求是否有效
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        login_form = LoginForm()
    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)

def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.changed_data['username']
            password = reg_form.changed_data['password']
            email = reg_form.changed_data['email']
            # 创建用户
            user = User.objects.create_user(username, email, password)
            user.save()
            # 登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        reg_form = RegForm()
    context = {}
    context['reg_form'] = reg_form
    return render(request, 'register.html', context)