from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib.auth import login, authenticate

from .forms import LoginForm
from .models import Items


class LoginPageView(View):
    template_name = 'budget/login.html'
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
        message = 'Login failed!'
        return render(request, self.template_name, context={'form': form, 'message': message})


class HomePageView(TemplateView):
    template_name = 'budget/main.html'
    model = Items

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['item_list'] = Items.objects.all()
        return context
