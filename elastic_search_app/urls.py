"""octolab_task URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from elastic_search_app import views

urlpatterns = [
    path('search/', views.SearchView.as_view(), name='search'),
    path('mapping/', views.MappingView.as_view(), name='mapping'),
    path('create-index/', views.CreateIndexView.as_view(), name='create_index'),
    path('add-data/', views.AddDataView.as_view(), name='add_data'),
    path('get-document/', views.GetDocumentView.as_view(), name='get_document'),
]
