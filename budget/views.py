from django.contrib.auth import authenticate, login
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, View

from .forms import LoginForm
from .helpers import get_month_param, get_months, get_selected_month
from .models import BaseConfig, Income, Items, UserSettings


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
        return render(request, self.template_name,
                      context={'form': form, 'message': message})

class HomePageView(TemplateView):
    template_name = 'budget/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        month_param = get_month_param(self.request)
        total_income_year = self.get_total_year()
        total_income_month = self.get_total_month()
        top_five_payments = self.top_five_payments(month_param)
        calculated_categories = self.get_calculated_categories(month_param)
        months = get_months()
        selected_month = get_selected_month(month_param)
        context['income'] = Income.objects.all()
        context['currency'] = BaseConfig.objects.all()
        # context['income_sum_year'] = total_income_year['income_year__sum']
        context['income_sum_year'] = 1000
        # context['income_sum_month'] = total_income_month['income_month__sum']
        context['income_sum_month'] = 22
        context['top_five_payments'] = top_five_payments
        context['calculated_categories'] = calculated_categories
        context['all_months'] = months
        context['selected_month'] = selected_month
        context['select_month_id'] = month_param
        return context

    def get_total_month(self):
        # FIXME: Sum is an issue with postgres
        # total_income = Income.objects.aggregate(Sum('income_month'))
        return 100

    def top_five_payments(self, pk):
        top_records = Items.objects.filter(month__pk=pk).order_by('value')[:5]
        return top_records

    def get_calculated_categories(self, pk):
        grouped = {}
        total_monthly_income = self.get_total_month()
        categories = Items.objects.filter(month=pk).\
            values_list('value', 'category')
        for x, y in categories:
            x = float(x)
            if y in grouped:
                grouped[y] += x
            else:
                grouped[y] = x
        for x, y in grouped.items():
            grouped[x] = (y / total_monthly_income['income_month__sum']) * 100
        return grouped

    def post(self, request, *args, **kwargs):
        if len(request.POST['month']) > 5:
            UserSettings.objects.create(month=request.POST['month'])
            return redirect('/home')
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

    def get_revenue_source(request):
        refenue_source = Income.objects.filter().\
            values_list('income_month', 'person')
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

    def get_total_year(self):
        # FIXME: Sum is an issue with postgres
        # total_income = Income.objects.aggregate(Sum('income_year'))
        return 100


class BreakdownPageView(TemplateView):
    template_name = 'budget/breakdown.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        months = get_months()
        month_id = get_month_param(self.request)
        selected_month = get_selected_month(month_id)
        expenses = self.get_expenses(month_id)
        context['currency'] = BaseConfig.objects.all()
        context['all_months'] = months
        context['selected_month'] = selected_month
        context['expenses'] = expenses
        return context

    def get_expenses(self, pk):
        """
        Get all expenses for the current period
        :param pk:
        :return:
        """
        records = Items.objects.filter(month__pk=pk).\
            order_by('value')
        return records

    def post(self, request, *args, **kwargs):
        if len(request.POST['month']) > 5:
            return redirect('/breakdown')
        UserSettings.objects.create(month=request.POST['month'])
        return redirect(f'/breakdown?month={request.POST["month"]}')
