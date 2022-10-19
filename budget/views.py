import json

from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView, View
from django.contrib.auth import login, authenticate
from django.db.models import Sum
from django.http import JsonResponse

from .forms import LoginForm
from .models import Items, Income, BaseConfig, Period, UserSettings


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
        month_param = self.get_month_param()
        total_income_year = self.get_total_year()
        total_income_month = self.get_total_month()
        top_five_payments = self.top_five_payments(month_param)
        calculated_categories = self.get_calculated_categories(month_param)
        months = self.get_months()
        selected_month = self.get_selected_month(month_param)
        context['income'] = Income.objects.all()
        context['currency'] = BaseConfig.objects.all()
        context['income_sum_year'] = total_income_year['income_year__sum']
        context['income_sum_month'] = total_income_month['income_month__sum']
        context['top_five_payments'] = top_five_payments
        context['calculated_categories'] = calculated_categories
        context['all_months'] = months
        context['selected_month'] = selected_month
        context['select_month_id'] = month_param
        return context

    def get_total_year(self):
        total_income = Income.objects.aggregate(Sum('income_year'))
        return total_income

    def get_total_month(self):
        total_income = Income.objects.aggregate(Sum('income_month'))
        return total_income

    def top_five_payments(self, pk):
        top_records = Items.objects.filter(month__pk=pk).order_by('value')[:5]
        return top_records

    def get_calculated_categories(self, pk):
        grouped = {}
        total_monthly_income = self.get_total_month()
        categories = Items.objects.filter(month=pk).values_list('value', 'category')
        for x, y in categories:
            x = float(x)
            if y in grouped:
                grouped[y] += x
            else:
                grouped[y] = x
        for x, y in grouped.items():
            grouped[x] = (y / total_monthly_income['income_month__sum']) * 100
        return grouped

    def get_months(self):
        months = Period.objects.all()
        return months

    def get_selected_month(self, pk):
        count_months = Period.objects.all()
        if count_months and pk is not None:
            selected_month = Period.objects.get(pk=pk)
            return selected_month
        # FIXME: Return something better here if pk does not exist as a get parameter
        return

    def post(self, request, *args, **kwargs):
        if len(request.POST['month']) > 5:
            UserSettings.objects.create(month=request.POST['month'])
            return redirect(f'/home')
        return redirect(f'/home?month={request.POST["month"]}')

    def ajax_get_expenses(request):
        expenses = Items.objects.filter().values_list('month', 'value')
        grouped = {}
        for x, y in expenses:
            x = x
            if y in grouped:
                grouped[y] += x
            else:
                grouped[y] = x
        data = {
            'expenses': [0, 200]
        }
        return JsonResponse(data)

    def get_refenue_source(request):
        refenue_source = Income.objects.filter().values_list('income_month', 'person')
        ref = []
        person = []
        for x, y in refenue_source:
            ref.append(x)
            person.append(y)
        data = {
            'refenue_source': ref,
            'label': person,
        }
        return JsonResponse(data)

    def get_month_param(self):
        month_id = self.request.GET.get('month')
        return month_id


class BreakdownPageView(TemplateView):
    template_name = 'budget/breakdown.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        months = self.get_months()
        month_id = self.get_month_param()
        selected_month = self.get_selected_month(month_id)
        expenses = self.get_expenses(month_id)
        context['currency'] = BaseConfig.objects.all()
        context['all_months'] = months
        context['selected_month'] = selected_month
        context['expenses'] = expenses
        return context

    def get_selected_month(self, pk):
        selected_month = Period.objects.filter(pk=pk).first()
        return selected_month

    def get_months(self):
        months = Period.objects.all()
        return months

    def get_expenses(self, pk):
        records = Items.objects.filter(month__pk=pk).order_by('value')
        return records

    def post(self, request, *args, **kwargs):
        if len(request.POST['month']) > 5:
            return redirect(f'/breakdown')
        UserSettings.objects.create(month=request.POST['month'])
        return redirect(f'/breakdown?month={request.POST["month"]}')

    def get_month_param(self):
        month_id = self.request.GET.get('month')
        return month_id
