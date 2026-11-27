from django.urls import path

from .views import ConsentListCreateView, ConsentWithdrawView

urlpatterns = [
    path("consent/", ConsentListCreateView.as_view(), name="consent-list-create"),
    path("consent/<uuid:pk>/withdraw/",ConsentWithdrawView.as_view(),name="consent-withdraw",),
]