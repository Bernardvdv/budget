from django.http import HttpResponse
from django.shortcuts import render


def index(render):
    return HttpResponse('Hello')
