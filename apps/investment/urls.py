from django.urls import path

from . import views
from ..helpers.views import staff_required

urlpatterns = [
    path('all/', staff_required(views.InvestmentListView.as_view()), name='all_investments'),
    path('add/', staff_required(views.InvestmentAddView.as_view()), name='investment-add'),
    path('<int:pk>/update/', views.investment_update, name='investment-update'),
    path('<int:pk>/delete/', views.investment_delete, name='investment-delete'),

]
