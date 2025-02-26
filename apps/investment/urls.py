from django.urls import path

from . import views
from .savings_status import ChangeSavingStatus
from ..helpers.views import staff_required

urlpatterns = [
    path('all/', staff_required(views.InvestmentListView.as_view()), name='all_investments'),
    path('add/', staff_required(views.InvestmentAddView.as_view()), name='investment-add'),
    path('<int:pk>/update/', views.investment_update, name='investment-update'),
    path('<int:pk>/delete/', views.investment_delete, name='investment-delete'),


    path('daily-saving-list/', staff_required(views.DailySavingListView.as_view()), name='daily-saving-list'),
    path('daily-saving-transaction/', staff_required(views.DailySavingTransactionView.as_view()),
         name='daily-saving-transaction'),
    path('change-saving-status/', ChangeSavingStatus.as_view(), name='change_saving_status'),
    path('daily-saving-add/', staff_required(views.DailySavingAddView.as_view()), name='daily-saving-add'),

]
