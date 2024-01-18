from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from guide.models import Guide


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
class GuidePageView(View):
    def get(self, request):
        guides = Guide.objects.all()
        context = {
            'guides': guides,
        }
        return render(request, 'system_guide/guide_page.html', context)