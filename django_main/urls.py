"""django_main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from kaijaing import views as myviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',myviews.login),
    path('foo/',myviews.foo),
    path('quanxian_get/',myviews.quanxian_get),
    path('user/',myviews.user),
    path('user_status/',myviews.user_status),
    path('add_user/',myviews.add_user),
    path('user_up_select/',myviews.user_up_select),
    path('user_update/',myviews.user_update),
    path('delete_user/',myviews.delete_user),
    path('color/',myviews.color),
    path('add_color/',myviews.add_color),
    path('color_up_select/',myviews.color_up_select),
    path('update_color/',myviews.update_color),
    path('delete_color/',myviews.delete_color),
    path('skutype/',myviews.skutype),
    path('add_skutype/',myviews.add_skutype),
    path('update_skutype/',myviews.update_skutype),
    path('skutype_select/',myviews.skutype_select),
    path('delete_skutype/',myviews.delete_skutype),
    path('sku/',myviews.sku),
    path('sku_status/',myviews.sku_status),
    path('sku_up_select/',myviews.sku_up_select),
    path('sku_update/',myviews.sku_update),
    path('type_select/',myviews.type_select),
    path('add_sku/',myviews.add_sku),
    path('delete_sku/',myviews.delete_sku),
    path('wuliu/',myviews.wuliu),
    path('add_wuliu/',myviews.add_wuliu),
    path('wuliu_up_select/',myviews.wuliu_up_select),
    path('update_wuliu/',myviews.update_wuliu),
    path('delete_wuliu/',myviews.delete_wuliu),
    path('wenzi/',myviews.wenzi),
    path('add_wenzi/',myviews.add_wenzi),
    path('wenzi_up_select/',myviews.wenzi_up_select),
    path('update_wenzi/',myviews.update_wenzi),
    path('delete_wenzi/',myviews.delete_wenzi),
    path('img/',myviews.img),
    path('delete_img/',myviews.delete_img),
    path('order/',myviews.order),
    path('order_sku/',myviews.order_sku),
    path('wenzi_order_select/',myviews.wenzi_order_select),
    path('wuliu_order_select/',myviews.wuliu_order_select),
    path('cop_order/',myviews.cop_order),
    path('order_save/',myviews.order_save),
    path('update_mima/',myviews.update_mima),
    path('page_get/',myviews.page_get),
    path('order_update/',myviews.order_update),
    path('test/',myviews.test),
    path('delete_order/',myviews.delete_order),
    path('order_Approval/',myviews.order_Approval),
    path('order_del/',myviews.order_del),
    path('draw_save/',myviews.draw_save),
    path('saleman/',myviews.saleman),
    path('packing_save/',myviews.packing_save),
    path('packing_list/',myviews.packing_list),
    path('order_out_one/',myviews.order_out_one),
    path('packing_pl/',myviews.packing_pl),
    path('roles/',myviews.roles),
    path('quanxian_list_all/',myviews.quanxian_list_all),
    path('role_check/',myviews.role_check),
    path('role_save/',myviews.role_save),
    path('role_new/',myviews.role_new),
    path('role_select/',myviews.role_select),
    path('update_role_select/',myviews.update_role_select),
    path('role_up_save/',myviews.role_up_save),
    path('delete_role/',myviews.delete_role),
    path('get_role/',myviews.get_role),
    path('packing_list_all/',myviews.packing_list_all),
    path('size/',myviews.size),
    path('size_up_select/',myviews.size_up_select),
    path('update_size/',myviews.update_size),
    path('add_size/',myviews.add_size),
    path('delete_size/',myviews.delete_size),
    path('style/',myviews.style),
    path('add_style/',myviews.add_style),
    path('style_up_select/',myviews.style_up_select),
    path('update_style/',myviews.update_style),
    path('delete_style/',myviews.delete_style),
    path('pack_method/',myviews.pack_method),
    path('packing_up_select/',myviews.packing_up_select),
    path('update_packing/',myviews.update_packing),
    path('add_packing/',myviews.add_packing),
    path('delete_packing/',myviews.delete_packing),
    path('packing_order_select/',myviews.packing_order_select),
    path('store_excel/',myviews.store_excel),
    path('excel_file_store/',myviews.excel_file_store),
    path('auto_store/',myviews.auto_store),
    path('order_del_draw/',myviews.order_del_draw),
    path('create_pi/',myviews.create_pi),
    path('draw_pi/',myviews.draw_pi),
    path('draw_page_get/',myviews.draw_page_get),
    path('delete_draw_pi/',myviews.delete_draw_pi),
    path('draw_Approval/',myviews.draw_Approval),
    path('order_complete/',myviews.order_complete),
    path('draw_agin/',myviews.draw_agin),
    path('draw_again_del/',myviews.draw_again_del),
    path('order_del_close/',myviews.order_del_close),
    path('print_status/',myviews.print_status),
    path('update_print_status/',myviews.update_print_status),
    path('style_select/',myviews.style_select),
    path('draw_list_all/',myviews.draw_list_all),
    path('order_track/',myviews.order_track),
    path('order_Approval_cancel/',myviews.order_Approval_cancel),
    path('warehouse/',myviews.warehouse),
    path('pur_order/',myviews.pur_order),
    path('contacts/',myviews.contacts),
    path('contacts_status/',myviews.contacts_status),
    path('add_contacts/',myviews.add_contacts),
    path('contacts_update/',myviews.contacts_update),
    path('delete_contacts/',myviews.delete_contacts),
    path('cl_sku/',myviews.cl_sku),
    path('add_cl_sku/',myviews.add_cl_sku),
    path('cl_sku_status/',myviews.cl_sku_status),
    path('cl_sku_update/',myviews.cl_sku_update),
    path('delete_cl_sku/',myviews.delete_cl_sku),
    path('pur_order_select/',myviews.pur_order_select),
    path('cl_order_sku/',myviews.cl_order_sku),
    path('cl_order_save/',myviews.cl_order_save),
    path('pur_page_get/',myviews.pur_page_get),
    path('cl_order_update/',myviews.cl_order_update),
    path('pur_Approval/',myviews.pur_Approval),
    path('Stock_del/',myviews.Stock_del),
    path('delete_ware/',myviews.delete_ware),
    path('install_lodop32/',myviews.install_lodop32),
    path('install_lodop64/',myviews.install_lodop64),
    path('CLodop_Setup_for_Win32NT/',myviews.CLodop_Setup_for_Win32NT),
    path('order_del_picture/',myviews.order_del_picture),
    path('warehouse_out/',myviews.warehouse_out),
    path('get_user_add/',myviews.get_user_add),
    path('size_order_select/',myviews.size_order_select),
    path('print_draw/',myviews.print_draw),
    path('get_user_name/',myviews.get_user_name),
    path('img_order/',myviews.img_order),
    path('draw_Approval_cancel/',myviews.draw_Approval_cancel),
    path('style_order_select/',myviews.style_order_select),
    path('excel_out/',myviews.excel_out),
    path('draw_print/',myviews.draw_print),
    path('update_draw/',myviews.update_draw),
]
