"""task1_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, re_path

from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from api import views


SchemaView = get_schema_view(
    openapi.Info(
        title="RocketData API",
        default_version='v1',
        description="RocketData test project api",
        contact=openapi.Contact(email="mpilkou@gmail.com"),
        license=openapi.License(name="Apache License Version 2.0"),
    ),
    public=True,
    permission_classes=(IsAuthenticatedOrReadOnly, ),
    authentication_classes=(SessionAuthentication, ),

)

urlpatterns = [
    path('', SchemaView.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('redoc/', SchemaView.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger/', SchemaView.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
        SchemaView.without_ui(cache_timeout=0), name='schema-json'),
    path('chain/', views.get_chains_network, name='chains'),
    path('chain/<int:chain_id>/delete', views.delete_chain, name='delete_chain'),
    path('chain/country/<str:country>', views.get_chains_by_country, name='chains_by_country'),
    path('chain/statictic/', views.get_chains_by_gt_avg_debt, name='gt_avg_debt'),
    path('product/<int:product_id>/contacts/', views.get_chain_contacts_by_product_id,
        name='contacts_by_product_id'),
]
