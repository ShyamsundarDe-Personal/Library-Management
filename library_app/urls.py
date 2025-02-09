from django.urls import path
from .views import *

urlpatterns = [
    path('', register_view),
    path('register/', register_view),
    path('login/', login_view),
    path('logout/', logout_view),
    path('pie-chart/', pie_chart_view, name='pie_chart'),
    path('home/', home),
    path('add-book/', add_book),
    path('add-book/add', view_book),
    path('edit-book/', edit_view_book),
    path('edit-book/edit', edit_book),
    path('delete-book/', delete_book),
]