from django.urls import path

from . import views
from ..helpers.views import staff_required

urlpatterns = [
    path('all/', staff_required(views.InvestmentListView.as_view()), name='all_investments'),

]
