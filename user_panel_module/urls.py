from django.urls import path

from . import views

urlpatterns = [
    path('' , views.UserPanelView.as_view() , name='user_panel_page'),
    path('edit-profile/' , views.EditUserProfilePage.as_view() , name='edit_profile'),
    path('change-password/' , views.ChangePasswordPage.as_view() , name='change_password'),
    path('my-shoppings/' , views.MyShoppings.as_view() , name='shoppings_list'),
    path('my-shopping-detail/<order_id>' , views.my_shopping_detail , name='shopping_detail_list'),
    path('user-basket/' , views.user_basket , name='user_basket'),
    path('remove-order-detail/' , views.remove_order_detail , name='remove_order_detail_ajax'),
    path('change_order_detail/', views.change_order_detail_count, name='change_order_detail_count_ajax')
]