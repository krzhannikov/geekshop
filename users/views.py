from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator

from .forms import UserLoginForm, UserRegisterForm, UserProfileForm, UserProfileEditForm
from django.views.generic.edit import CreateView, UpdateView
from baskets.models import Basket


# Create your views here.
from .models import User, UserProfile


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    success_url = 'index'
    # success_url = reverse_lazy('products:index')
    # using instead LOGIN_REDIRECT_URL in settings

    def get(self, request, *args, **kwargs):
        sup = super(UserLoginView, self).get(request, *args, **kwargs)
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy(self.success_url))
        return sup

    def get_context_data(self, **kwargs):
        context = super(UserLoginView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Авторизация'
        return context


# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user and user.is_active:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#     else:
#         form = UserLoginForm()
#     context = {
#         'title': 'GeekShop - Авторизация',
#         'form': form
#     }
#
#     return render(request, 'users/login.html', context)


class UserCreateView(CreateView):
    model = User
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Регистрация'
        return context


# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(data=request.POST)
#         if form.is_valid():
#             user = form.save()
#             if send_verify_link(user):
#                 messages.success(request, 'Вы успешно зарегистрированы')
#             return HttpResponseRedirect(reverse('users:login'))
#     else:
#         form = UserRegisterForm()
#     context = {
#         'title': 'GeekShop - Регистрация',
#         'form': form
#     }
#
#     return render(request, 'users/register.html', context)


class UserUpdateView(UpdateView):
    model = User
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    form_class_vk = UserProfileEditForm
    success_url = reverse_lazy('users:profile')
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Профиль'
        context['profile_form'] = self.form_class_vk(instance=self.request.user.userprofile)
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserUpdateView, self).dispatch(request, *args, **kwargs)

    def get_object(self, *args, **kwargs):
        return get_object_or_404(User, pk=self.request.user.pk)

    @transaction.atomic
    def post(self, request, *args, **kwargs):  # отвечает за сохранение формы
        user = self.get_object()
        edit_form = UserProfileForm(data=request.POST, files=request.FILES, instance=user)
        profile_form = UserProfileEditForm(data=request.POST, files=request.FILES, instance=user.userprofile)

        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(self.success_url)

        return render(request, self.template_name, {
            'form': edit_form,
            'profile_form': profile_form,
        })


# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(data=request.POST, instance=request.user, files=request.FILES)
#         profile_form = UserProfileEditForm(data=request.POST, instance=request.user.userprofile)
#         if form.is_valid() and profile_form.is_valid():
#             form.save()
#             messages.success(request, 'Профиль успешно обновлён')
#             return HttpResponseRedirect(reverse('users:profile'))
#     else:
#         profile_form = UserProfileEditForm(instance=request.user.userprofile)
#         form = UserProfileForm(instance=request.user)
#     context = {
#         'title': 'GeekShop - Профиль',
#         'form': form,
#         'profile_form': profile_form,
#         # 'baskets': Basket.objects.filter(user=request.user)
#     }
#
#     return render(request, 'users/profile.html', context)


def send_verify_link(user):
    verify_link = reverse('users:verify', args=[user.email, user.activation_key])
    subject = f'Для активации учетной записи {user.username} пройдите по ссылке'
    message = f'Для подтверждения учетной записи {user.username} на портале \n {settings.DOMAIN_NAME}{verify_link}'
    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key):
    try:
        user = User.objects.get(email=email)
        if user and user.activation_key == activation_key and not user.is_activation_key_expired():
            user.activation_key = ''
            user.activation_key_expires = None
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return render(request, 'users/verification.html')
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
