from django.urls import path
from . import views


urlpatterns = [

    path('add/',views.intake_add,name='add'),
    path('list/',views.intake_list,name='list'),
    path('edit/<int:pk>/',views.intake_update,name='edit'),
    path('delete/<int:pk>/',views.intake_delete,name='delete'),
    path('difference/',views.calculate_difference,name='calculate'),
    path('calc/',views.view_calc,name='calc')
]
