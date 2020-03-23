"""rctest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from recruit import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
                  path('signup/', views.SignupView.as_view(), name='signup'),
                  path('admin/', admin.site.urls),
                  path('', views.CustomLoginView.as_view(), name="main"),
                  path('signout/', views.signout, name="signout"),
                  path('notice/', views.notice, name="notice"),
                  path('new', views.NewView.as_view(), name="new"),
                  path('show', views.ShowView.as_view(), name="show"),
                  path('edit/<int:pk>', views.EditView.as_view(), name="edit"),
                  path('profile_update/<int:pk>', views.UserUpdate.as_view(), name="profile_update"),
                  path('submit', views.submit, name="submit"),
                  path('delete', views.delete, name="delete"),
                  path('guide', views.guide, name="guide"),
                  path('faq', views.faq, name="faq"),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)