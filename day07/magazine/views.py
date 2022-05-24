from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import DatabaseError
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from typing import Any, Dict

from django.views.generic import ListView, RedirectView, FormView, DetailView, \
    CreateView

from .models import Article, UserFavouriteArticle
from .forms import LoginForm, FavouriteForm, PublishForm
from django.http import HttpResponse


class Home(RedirectView):
    url = reverse_lazy('articles')


class ArticlesView(ListView):
    template_name = "articles.html"
    model = Article
    queryset = Article.objects.filter().order_by('-created')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context


class Login(FormView):
    template_name = "login.html"
    form_class = LoginForm
    success_url = reverse_lazy('index')

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if self.request.user.is_authenticated:
            messages.error(self.request, 'You are already logged in!')
            return redirect('index')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form: LoginForm):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user is None:
            messages.error(self.request, "Invalid username or password.")
            return
        login(self.request, user)
        messages.info(self.request, f"You are now logged in as {username}.")
        return super().form_valid(form)


class Publications(LoginRequiredMixin, ListView):
    template_name = "publications.html"
    model = Article
    login_url = reverse_lazy('login')

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)


class Favourite(LoginRequiredMixin, ListView):
    template_name = "favourite.html"
    login_url = reverse_lazy('login')
    model: UserFavouriteArticle = UserFavouriteArticle

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class Logout(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('index')
    login_url = reverse_lazy('index')

    def get_redirect_url(self, *args: Any, **kwargs: Any):
        logout(self.request)
        return super().get_redirect_url(*args, **kwargs)


class Detail(DetailView):
    template_name = "detail.html"
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = context['object']
        context["favouriteForm"] = FavouriteForm(article.id)
        return context


class Register(CreateView):
    template_name = "register.html"
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            return redirect('index')
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return super().get(request, *args, **kwargs)


class Publish(LoginRequiredMixin, CreateView):
    template_name = "publish.html"
    model = Article
    fields = [
        'title',
        'synopsis',
        'content',
    ]
    success_url = reverse_lazy('index')
    login_url = reverse_lazy('login')

    def form_valid(self, form: PublishForm):
        try:
            form.instance.author = self.request.user
            resp = super().form_valid(form)
            messages.success(self.request, "Successful publish.")
            return resp
        except DatabaseError as e:
            messages.success(
                self.request, "Unsuccessful publish. DatabaseError")
            return redirect('index')

    def form_invalid(self, form):
        messages.error(
            self.request, "Unsuccessful publish. Invalid information.")
        return super().form_invalid(form)


class AddToFavourite(LoginRequiredMixin, CreateView):
    model = UserFavouriteArticle
    fields = []
    success_url = reverse_lazy('index')
    login_url = reverse_lazy('login')

    def form_valid(self, form: PublishForm):
        article_id = form.data.get('article_id')
        ufa = UserFavouriteArticle.objects.filter(
            article=article_id, user=self.request.user)
        if ufa:
            ufa.delete()
            messages.success(
                self.request, "successful Remove to favourite.")
            return HttpResponseRedirect(self.success_url)

        try:
            article = Article.objects.get(pk=form.data.get('article_id'))
            form.instance.user = self.request.user
            form.instance.article = article
            resp = super().form_valid(form)
            messages.success(
                self.request, "successful Add to favourite.")
            return resp

        except DatabaseError as e:
            messages.error(
                self.request,
                "Unsuccessful Add to favourite. Database error."
            )

