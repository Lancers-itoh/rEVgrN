"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import include, path

urlpatterns = [
    # https://docs.djangoproject.com/en/2.0/topics/auth/default/#module-django.contrib.auth.views
    path('', include('blogs.urls')),
    path('adminuser/', include('smsusers.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]

#django.contrib.auth.urls をインクルードすれば、templates/registration/以下に配置された
#login.htmlおよびlogged_out.htmlという名前のテンプレートが、それぞれ上記URLにおいて自動的に表示される
