from django.shortcuts import render
from django.views import View

from accounts.models import SiteRules


class RulesSite(View):
    def get(self, request):
        list_rules = SiteRules.objects.all()
        context = {
            "list_rules": list_rules,
        }
        return render(request, 'rules_site.html', context)