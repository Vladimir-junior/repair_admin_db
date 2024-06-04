# from django.contrib import admin
from django.urls import path


from users.admin import site
from users.views import main, check_status, add_order, order_success

urlpatterns = [
    path('admin/', site.urls, name="admin"),
    path('', main,name="main"),
    path('status/', check_status, name='check_status'),
    path('add_order/', add_order, name='add_order'),
    path('order_success/', order_success, name='order_success'),

]


# from django.contrib import admin
# from django.urls import path
# from users.admin import site
# from users.views import main
#
# urlpatterns = [
#     path('', main,name="main"),
#     path('admin/', admin.site.urls, name='admin_panel'),
# ]

