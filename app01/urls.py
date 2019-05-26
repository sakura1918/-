from django.urls import path
from app01 import views

app_name = 'app01'

urlpatterns = [
    path('index/', views.index,name='index'),
    path('bookdetails/',views.bookdetails,name='bookdetails'),
    path('registeok/',views.registeok,name='registeok'),
    path('regist/',views.regist, name = 'regist'),
    path('regist_handle/',views.regist_handle, name = 'regist_handle'),
    path('getcaptcha/',views.getcaptcha,name = 'getcaptcha'),
    path('checkname/',views.checkname,name = 'checkname'),
    path('checkpwd/',views.checkpwd,name = 'checkpwd'),
    path('checknum/',views.checknum,name = 'checknum'),
    path('checkallow/',views.checkallow,name = 'checkallow'),
    path('login/',views.login,name = 'login'),
    path('login_logic/',views.login_logic,name="login_logic"),
    path('list/',views.list,name = "list"),
    path('indent/',views.indent,name = "indent"),
    path('indentok/',views.indentok,name = "indentok"),
    path('add_book/', views.add_book, name="add_book"),
    path('shoudong/', views.shoudong, name="shoudong"),
    path('shoppingcar/',views.shoppingcar,name = 'shoppingcar'),
    path('registeok/',views.registeok,name = 'registeok'),
    path('shopadd/',views.shopadd,name = 'shopadd'),
    path('shopdel/',views.shopdel,name = 'shopdel'),
    path('delete_s/',views.delete_s,name = 'delete_s'),
    path('arrive_form/', views.arrive_form,name ='arrive_form' ),
    path('user_register/', views.user_register,name = 'user_register'),
    path('confirm/', views.user_confirm,name = 'user_confirm')
]