from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from ptup_utilities.views import RulesSite

urlpatterns = [
    path('admin/', admin.site.urls),

    path('header', views.header, name="header"),
    path('footer', views.footer, name="footer"),

    path('', views.home, name="home"),
    path('page_404/', views.page_404, name="page_404"),
    path('site_rules/', RulesSite.as_view(), name="site_rules"),

    # apps
    path('accounts/', include("accounts.urls")),
    path('customers/', include("customers.urls")),
    path('doctors/', include("doctors.urls")),
    path('messages/', include("ptup_messages.urls")),
    path('illness/', include("illness.urls")),
    path('content/', include("healing_content.urls")),
    path('foundation_course/', include("foundation_course.urls")),
    path('followup/', include("followup.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)