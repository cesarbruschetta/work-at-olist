"""billing_phonecalls URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url='/docs/index.html', permanent=False), name='index'),
    path('admin/', admin.site.urls),
    path('api/', include('billing_phonecalls.core.urls')),
    path('docs/', RedirectView.as_view(url='/docs/index.html', permanent=False), name='index-doc'),
] + static(settings.DOCS_URL, document_root=settings.DOCS_ROOT)
