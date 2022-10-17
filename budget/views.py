import json

from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib.auth import login, authenticate
from django.db.models import Sum

from .forms import LoginForm
from .models import Items, Income, BaseConfig


class LoginPageView(View):
    template_name = 'budget/login.html'
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_income_year = self.get_total_year()
        total_income_month = self.get_total_month()
        top_five_payments = self.top_five_payments()
        calculated_categories = self.get_calculated_categories()
        test = [0, 200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200]
        context['income'] = Income.objects.all()
        context['currency'] = BaseConfig.objects.all()
        context['income_sum_year'] = total_income_year['income_year__sum']
        context['income_sum_month'] = total_income_month['income_month__sum']
        context['top_five_payments'] = top_five_payments
        context['expenses_chart'] = json.dumps(test)
        return context

    def get_total_year(self):
        total_income = Income.objects.aggregate(Sum('income_year'))
        return total_income

    def get_total_month(self):
        total_income = Income.objects.aggregate(Sum('income_month'))
        return total_income

    def top_five_payments(self):
        top_records = Items.objects.filter().order_by('value')[:5]
        return top_records

    def get_calculated_categories(self):
        total_monthly_income = self.get_total_month()
        categories = Items.objects.filter().values_list('value', 'category')
        print(categories)


