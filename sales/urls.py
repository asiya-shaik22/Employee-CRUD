from django.urls import path

from sales import views

urlpatterns = [
    path('',views.login_fun,name='log'),
    path('signup/',views.signup_fun,name='signup'),
    path('home/',views.home,name='home'),
    path('add/',views.add_emp,name='add'),
    path('display/',views.display_emp,name='display'),
    path('update/<int:id>',views.update_emp,name='update'),
    path('delete/<int:id>',views.delete_emp,name='delete')

 ]