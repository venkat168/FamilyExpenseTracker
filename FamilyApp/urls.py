from django.urls import path

from FamilyApp import views

urlpatterns=[

    path('',views.log_fun,name='log'),
    path('logdata',views.logdata_fun),
    path('reg',views.reg_fun,name='reg'),
    path('regdata',views.regdata_fun),
    path('home',views.go_to_home,name='home'),
    path('addfamily', views.add_family, name='addfamily'),
    path('addingmember',views.adding_member,name='addingmember'),
    path('seefamily',views.seefamily,name='seefamily'),
    path('updatemem/<int:id>', views.update_family_mem, name="update"),
    path('delmem/<int:id>', views.del_family_mem, name="delete"),
    path('addexp', views.add_expenses, name='addexp'),
    path('saveexpensedata',views.save_expense_data,name='saveexpenses'),
    path('viewexpense', views.view_expenses, name="viewexpense"),
    path('updateExpenses/<int:id>', views.update_expenses, name="updateexpense")


]