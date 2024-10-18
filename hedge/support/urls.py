from django.urls import path
from . import views
from .views import *

from django.urls import re_path

urlpatterns = [
    path('api/query', SupportView.as_view(), name='save_support'),
    path('api/view/query/<int:support_id>', views.support_data_details, name='support_data_details'),
    path('api/update/query', views.support_data_change_status, name='support_data_change_status'),
    path('api/view/message/<int:support_id>', views.support_data_message, name='support_data_message'),
    path('api/add/message/<int:support_id>', views.save_support_message, name='save_support_message'),
    path('api/delete/query/<int:support_id>', views.support_data_delete, name='support_data_delete'),
    

]
