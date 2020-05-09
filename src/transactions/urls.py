from django.urls import path
from .views import (
    transaction_upload,
    transaction_detail_view,
    TransactionCreateClassView,
    transaction_update_view,
    transaction_delete_view,
    TransactionListClassView,
    TransactionFilteredListClassView,
)

app_name = "transactions"

urlpatterns = [
    path("upload/", transaction_upload, name="Transaction (Upload)"),
    path('<int:requested_id>/', transaction_detail_view, name='Transaction'),
    path('create/', TransactionCreateClassView.as_view(),
         name='Transaction (Create)'),
    path('<int:requested_id>/update/',
         transaction_update_view, name='Transaction (Update)'),
    path('<int:requested_id>/delete/',
         transaction_delete_view, name='Transaction (Delete)'),
    path('transactions_list_view/', TransactionListClassView.as_view(),
         name="Transaction List View"),
    #     path('transactions_list_view/<int:year>-<int:month>-<int:day>', TransactionFilteredListClassView.as_view(),
    #          name="Transaction List View (Filtered)")
]
