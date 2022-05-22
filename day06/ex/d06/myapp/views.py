from django.shortcuts import render
from django.views import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import DatabaseError
from django.http import HttpRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from django import db
from .forms import TipForm, DeleteTipForm, VoteForm, NewUserForm
from .models import TipModel


class Index(View):
    template_name = "index.html"

    def get(self, request):
        try:
            tips = TipModel.objects.all().order_by('-date')

        except db.DatabaseError as e:
            tips = []
        context = {
            'tipform': TipForm(),
            'tips': [{
                'id': tip.id,
                'content': tip.content,
                'author': tip.author,
                'date': tip.date,
                'up_votes': tip.up_votes,
                'down_votes': tip.down_votes,
                'deleteform': DeleteTipForm(tip.id),
                'voteform': VoteForm(tip.id),
            } for tip in tips],
        }
        return render(request, self.template_name, context)


class Registration(FormView):
    template_name = "registration.html"
    form_class = NewUserForm
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('index')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form: UserCreationForm):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Registration successful.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Unsuccessful registration. Invalid information."
        )
        return super().form_invalid(form)


class Login(FormView):
    template_name = "login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('index')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form: AuthenticationForm):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user is None:
            messages.error(self.request, "Invalid username or password.")
            return
        login(self.request, user)

        messages.info(self.request, f"You are now logged in as {username}.")
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class Logout(View):
    template_name = "index.html"

    def get(self, request):
        logout(request)
        messages.info(request, "You have successfully logged out.")
        return redirect('index')


class Tip(LoginRequiredMixin, View):
    http_method_names = ['post', 'put', 'delete']
    login_url = reverse_lazy('login')

    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        if method == 'put':
            return self.put(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(Tip, self).dispatch(*args, **kwargs)

    def post(self, request):
        form = TipForm(request.POST)
        if form.is_valid():
            try:
                TipModel.objects.create(
                    content=form.cleaned_data['content'],
                    author=request.user
                )
                messages.success(self.request, "Successful create Tip.")
            except DatabaseError as e:
                print(e)
                messages.error(
                    self.request, "Unsuccessful create Tip. (db error)")
        else:
            messages.error(
                self.request, "Unsuccessful create Tip. (Invalid form data.)")
        return redirect('index')

    def __error_msg(self, method, msg):
        messages.error(
            self.request, f"Unsuccessful {method} Tip. ({msg})")
        return redirect('index')

    def delete(self, request: HttpRequest):
        form = DeleteTipForm(None, request.POST)
        if not form.is_valid():
            return self.__error_msg("delete", "Invalid form data.")
        try:
            tip: TipModel = TipModel.objects.get(
                id=form.cleaned_data['id'])
            if not (request.user.has_perm('myapp.delete_tipmodel')
                    or request.user == tip.author):
                return self.__error_msg("delete", "access denied")
            tip.delete()
            messages.success(self.request, "Successful delete Tip.")
        except TipModel.DoesNotExist as e:
            return self.__error_msg("delete", "Tip does not exist")
        except DatabaseError as e:
            return self.__error_msg("delete", "db error")

        return redirect('index')

    def put(self, request):
        form = VoteForm(None, request.POST)
        if not form.is_valid():
            return self.__error_msg("vote", "Invalid form data.")
        try:
            tip: TipModel = TipModel.objects.get(id=form.cleaned_data['id'])
            if form.cleaned_data['type']:
                tip.upvote(request.user)
                tip.author.increase_rep()
            elif tip.author != request.user and not request.user.has_perm('myapp.can_down_vote'):
                return self.__error_msg("vote", "you can't do that!!")
            else:
                tip.downvote(request.user)
                tip.author.decrease_rep()
        except TipModel.DoesNotExist as e:
            return self.__error_msg("vote", "Tip does not exist")
        except DatabaseError as e:
            return self.__error_msg("vote", "db error")
        messages.success(request, 'Voted success!')
        return redirect('index')
