# backend/views.py
import os
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.conf import settings

class FrontendAppView(TemplateView):
    template_name = "index.html"