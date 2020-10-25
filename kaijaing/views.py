from django.shortcuts import render,HttpResponse
from django.http import JsonResponse,FileResponse  #引入json响应
import json,requests
import os,django,time,datetime
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")# project_name 项目名称   #出现报错
django.setup()
from django.middleware.csrf import get_token
from kaijaing.models import User,quanxian,Color,SkuType,SKU,Wuliu,Wenzi,Order,Order_Del,packing,Roles,Roles_Del,Size,Style,Pack_method,Draw_Pi,Warehousing,Warehous_Del,Contacts,cl_SKU,Stock
from django.core.paginator import Paginator   #导入分页器
from django.db.models import Q
from django_main.settings import MEDIA_ROOT  #文件地址
import  hashlib,xlrd,xlwt
from kaijaing.sql import  pysql,pysql_update
from  django.utils.encoding import escape_uri_path

# Create your views here.

def login(request):
    post_data=request.body
    post_data=json.loads(post_data)
    print(post_data)
    login_user=User.objects.filter(name=post_data.get('form_data').get('username'),password=post_data.get('form_data').get('password'))
    if login_user:
    #判断登录号是否存在:
        token=get_token(request)  #得到token
        print(token)
        request.session['token']=token
        return HttpResponse('OK')
    else:
        return HttpResponse('404')
def quanxian_get(request):    #获取权限
    post_data = request.body
    post_data = json.loads(post_data)
    name=post_data.get('name')
    quanxian_list = [] #先定义
    if name and name != 'admin':
        role=User.objects.filter(name=name).values('role')  #获得角色名称
        quanxian_list = Roles_Del.objects.filter(role_name=role[0].get('role')).values().order_by('sort')
    elif name and name == 'admin':
        quanxian_list = quanxian.objects.all().values().order_by('sort')
    quanxian_json = []
    for quanxian_i in quanxian_list:
        quanxian_json.append(quanxian_i)
    dict = {}
    list = []  # 最终结果集合
    chiid_dict={}  #子菜单
    chiid_list=[]  #子菜单

    for quanxian_j in quanxian_json:
        #print(quanxian_j)
        if quanxian_j.get('level') == '0':  #一级菜单
            dict['id']=quanxian_j.get('jon_code')
            dict['name']=quanxian_j.get('job_name')
            for quanxian_h in quanxian_json:
                if int(quanxian_h.get('jon_code')[0]) == int(quanxian_j.get('jon_code')) and quanxian_h.get('jon_code') != quanxian_j.get('jon_code') and quanxian_h.get('level') == '1':
                    chiid_dict['id']=quanxian_h.get('jon_code')
                    chiid_dict['name']=quanxian_h.get('job_name')
                    chiid_list.append(chiid_dict)   #完成子集合
                    chiid_dict={}  #完成清空
            dict['children']=chiid_list
            chiid_list=[]   #完成清空
            list.append(dict)
            dict={}    #清空结果集合
    return JsonResponse(data=list,safe=False)
def foo(request):   #获取原生的django_token
    csrf_token=get_token(request)
    #print(csrf_token)
    return HttpResponse(csrf_token)

def user(request):    #获取用户信息
    post_data = request.body
    post_data = json.loads(post_data)
    user_json = []
    user_data={}
    if post_data.get('serch') == '' or post_data.get('serch') is None:
        user_list=User.objects.all().values()
    else:
        user_list = User.objects.filter(Q(name__icontains=post_data.get('serch'))|Q(nameid__icontains=post_data.get('serch'))).values()
    user_page=Paginator(user_list,post_data.get('size')).page(post_data.get('page'))
    total= Paginator(user_list,post_data.get('size')).count    #总计的数量
    for user_i in user_page:
        user_json.append(user_i)
    user_data['user_list']=user_json
    user_data['total']=total
    return JsonResponse(data=user_data,safe=False)
def order(request):    #获取订单信息
    #有权限区分,不同的人看到订单内容是不一样的
    post_data = request.body
    post_data = json.loads(post_data)
    user_id = post_data.get('user') #当前用户的账号信息
    selectForm = post_data.get('serch')
    #获取用户的详细信息
    user_info =User.objects.filter(name=user_id).values()
    user_address = user_info[0].get('address')  #获取地区
    user_radio = user_info[0].get('radio') #获取用户订单权限
    user_json = []
    user_data={}
    if user_radio == '3': #标识全部订单
        if selectForm.get('input') == '' and selectForm.get('date') == '' and selectForm.get('draw_status') == '' and selectForm.get('status') == '':
            user_list=Order.objects.all().values().order_by('-id')
        else:
            user_list = Order.objects.all().values().order_by('-id')
            if selectForm.get('input'):
                user_list = user_list.filter(Q(id__icontains=selectForm.get('input'))|Q(date__icontains=selectForm.get('input'))|Q(add__icontains=selectForm.get('input'))|Q(salesman__icontains=selectForm.get('input')))
            if selectForm.get('date'):
                draw_time = selectForm.get('date')
                begin_draw = draw_time[0][:10] + ' 00:00'
                end_draw = draw_time[1][:10] + ' 24:00'
                user_list = user_list.filter(create_time__gte=begin_draw, create_time__lte=end_draw)
            if selectForm.get('draw_status'):
                user_list = user_list.filter(draw_status= selectForm.get('draw_status'))
            if selectForm.get('status'):
                user_list = user_list.filter(status= selectForm.get('status'))

        user_page=Paginator(user_list,post_data.get('size')).page(post_data.get('page'))
    elif user_radio == '2': #标识本地区所有的订单
        if selectForm.get('input') == '' and selectForm.get('date') == '' and selectForm.get('draw_status') == '' and selectForm.get('status') == '':
            user_list=Order.objects.filter(add=user_address).values().order_by('-id')
        else:
            user_list=Order.objects.filter(add=user_address).values().order_by('-id')
            if selectForm.get('input'):
                user_list = user_list.filter(
                    Q(id__icontains=selectForm.get('input')) | Q(date__icontains=selectForm.get('input')) | Q(
                        add__icontains=selectForm.get('input')) | Q(salesman__icontains=selectForm.get('input')))
            if selectForm.get('date'):
                draw_time = selectForm.get('date')
                begin_draw = draw_time[0][:10] + ' 00:00'
                end_draw = draw_time[1][:10] + ' 24:00'
                user_list = user_list.filter(create_time__gte=begin_draw, create_time__lte=end_draw)
            if selectForm.get('draw_status'):
                user_list = user_list.filter(draw_status=selectForm.get('draw_status'))
            if selectForm.get('status'):
                user_list = user_list.filter(status=selectForm.get('status'))

        user_page = Paginator(user_list, post_data.get('size')).page(post_data.get('page'))
        user_page=Paginator(user_list,post_data.get('size')).page(post_data.get('page'))
    elif user_radio == '1': #标识自由自己的订单
        if selectForm.get('input') == '' and selectForm.get('date') == '' and selectForm.get('draw_status') == '' and selectForm.get('status') == '':
            user_list=Order.objects.filter(create_user=user_id).values().order_by('-id')
        else:
            user_list=Order.objects.filter(create_user=user_id).values().order_by('-id')
            if selectForm.get('input'):
                user_list = user_list.filter(
                    Q(id__icontains=selectForm.get('input')) | Q(date__icontains=selectForm.get('input')) | Q(
                        add__icontains=selectForm.get('input')) | Q(salesman__icontains=selectForm.get('input')))
            if selectForm.get('date'):
                draw_time = selectForm.get('date')
                begin_draw = draw_time[0][:10] + ' 00:00'
                end_draw = draw_time[1][:10] + ' 24:00'
                user_list = user_list.filter(create_time__gte=begin_draw, create_time__lte=end_draw)
            if selectForm.get('draw_status'):
                user_list = user_list.filter(draw_status=selectForm.get('draw_status'))
            if selectForm.get('status'):
                user_list = user_list.filter(status=selectForm.get('status'))
        user_page=Paginator(user_list,post_data.get('size')).page(post_data.get('page'))
    total= Paginator(user_list,post_data.get('size')).count    #总计的数量
    #for user_i in user_page:
        #user_json.append(user_i)
    user_data['user_list']=list(user_page)
    user_data['total']=total
    return JsonResponse(data=user_data,safe=False)
def user_status(request):
    post_data = request.body
    post_data = json.loads(post_data)
    try:
        user_updade=User.objects.filter(name=post_data.get('name')).update(status=post_data.get('status_c'))
        return HttpResponse('OK')
    except:
        return HttpResponse('NOT OK')
def add_user(request):
    post_data=request.body
    post_data=json.loads(post_data).get('form_data')
    #print(post_data)
    try:
        user_add=User(name=post_data.get('username'),nameid=post_data.get('password'),password='88888888',email=post_data.get('email'),iphone=post_data.get('iphone'),address=post_data.get('address'),role=post_data.get('role'),radio=post_data.get('radio'))
        user_add.save()
        return HttpResponse('OK')
    except:
        return HttpResponse('NOT OK')
def user_up_select(request):
    post_data = request.body
    post_data = json.loads(post_data)
    name=post_data.get('id')  #获得前段的用户编号字段
    user_json={}  #返回信息
    try:
        user_list=User.objects.filter(name=name).values()
        for user_i in user_list :
            user_json['name']=user_i.get('name')
            user_json['nameid']=user_i.get('nameid')
            user_json['email']=user_i.get('email')
            user_json['iphone']=user_i.get('iphone')
            user_json['address']=user_i.get('address')
            user_json['role']=user_i.get('role')
            user_json['radio']=user_i.get('radio')
        return JsonResponse(data=user_json,safe=False)
    except:
        return HttpResponse('NOT OK')
def user_update(request):
    post_data = request.body
    post_data = json.loads(post_data).get('data')
    try:
        User.objects.filter(name=post_data.get('name')).update(nameid=post_data.get('nameid'),email=post_data.get('email'),iphone=post_data.get('iphone'),address=post_data.get('address'),role=post_data.get('role'),radio=post_data.get('radio'))
        return HttpResponse('OK')
    except:
        return HttpResponse('NOT OK')
def delete_user(request): #删除用户
    post_data = request.body
    name = json.loads(post_data).get('name')
    try:
        User.objects.filter(name=name).delete()
        return HttpResponse('OK')
    except:
        return HttpResponse('NOT OK')
def color(request):
    color_list=Color.objects.all().values()   #获得全部信息
    color_json = []
    for color_i in color_list:
        color_json.append(color_i)
    return JsonResponse(data=color_json,safe=False)
def size(request):
    color_list=Size.objects.all().values()   #获得全部信息
    color_json = []
    for color_i in color_list:
        color_json.append(color_i)
    return JsonResponse(data=color_json,safe=False)
def pack_method(request):
    color_list=Pack_method.objects.all().values()   #获得全部信息
    color_json = []
    for color_i in color_list:
        color_json.append(color_i)
    return JsonResponse(data=color_json,safe=False)
def style(request):
    color_list=Style.objects.all().values()   #获得全部信息
    color_json = []
    for color_i in color_list:
        color_json.append(color_i)
    return JsonResponse(data=color_json,safe=False)
def add_color(request):
    post_data=request.body
    post_data=json.loads(post_data).get('form_data')
    #print(post_data)
    try:
        color_add=Color(color_id=post_data.get('color_id'),color_name=post_data.get('color_name'))
        color_add.save()
        return HttpResponse('OK')
    except:
        return HttpResponse('NOT OK')
def add_size(request):
    post_data=request.body
    post_data=json.loads(post_data).get('form_data')
    #print(post_data)
    try:
        color_add=Size(size_id=post_data.get('size_id'),size_name=post_data.get('size_name'))
        color_add.save()
        return HttpResponse('OK')
    except:
        return HttpResponse('NOT OK')
def add_style(request):
    post_data=request.body
    post_data=json.loads(post_data).get('form_data')
    #print(post_data)
    try:
        color_add=Style(id=post_data.get('id'),name=post_data.get('name'))
        color_add.save()
        return HttpResponse('OK')
    except:
        return HttpResponse('NOT OK')


def add_packing(request):
    post_data=request.body
    post_data=json.loads(post_data).get('form_data')
    #print(post_data)
    try:
        color_add=Pack_method(id=post_data.get('id'),name=post_data.get('name'))
        color_add.save()
        return HttpResponse('OK')
    except:
        return HttpResponse('NOT OK')
def add_wuliu(request):
    post_data=request.body
    post_data=json.loads(post_data).get('form_data')
    #print(post_data)
    try:
        color_add=Wuliu(id=post_data.get('color_id'),name=post_data.get('color_name'))
        color_add.save()
        return HttpResponse('OK')
    except:
        return HttpResponse('NOT OK')
def add_wenzi(request):
    post_data=request.body
    post_data=json.loads(post_data).get('form_data')
    #print(post_data)
    try:
        color_add=Wenzi(id=post_data.get('id'),name=post_data.get('name'))
        color_add.save()
        return HttpResponse('OK')
    except:
        return HttpResponse('NOT OK')
def color_up_select(request):
    post_data = request.body
    post_data = json.loads(post_data)
    name=post_data.get('id')  #获得前段的用户编号字段
    user_json={}  #返回信息
    try:
        user_list=Color.objects.filter(color_id=name).values()
        for user_i in user_list :
            user_json['color_id']=user_i.get('color_id')
            user_json['color_name']=user_i.get('color_name')
        return JsonResponse(data=user_json,safe=False)
    except:
        return HttpResponse('NOT OK')
def size_up_select(request):
    post_data = request.body
    post_data = json.loads(post_data)
    name=post_data.get('id')  #获得前段的用户编号字段
    user_json={}  #返回信息
    try:
        user_list=Size.objects.filter(size_id=name).values()
        for user_i in user_list :
            user_json['size_id']=user_i.get('size_id')
            user_json['size_name']=user_i.get('size_name')
        return JsonResponse(data=user_json,safe=False)
    except:
        return HttpResponse('NOT OK')
def style_up_select(request):
    post_data = request.body
    post_data = json.loads(post_data)
    name=post_data.get('id')  #获得前段的用户编号字段
    user_json={}  #返回信息
    try:
        user_list=Style.objects.filter(id=name).values()
        for user_i in user_list :
            user_json['id']=user_i.get('id')
            user_json['name']=user_i.get('name')
        return JsonResponse(data=user_json,safe=False)
    except:
        return HttpResponse('NOT OK')
def packing_up_select(request):
    post_data = request.body
    post_data = json.loads(post_data)
    name=post_data.get('id')  #获得前段的用户编号字段
    user_json={}  #返回信息
    try:
        user_list=Pack_method.objects.filter(id=name).values()
        for user_i in user_list :
            user_json['id']=user_i.get('id')
            user_json['name']=user_i.get('name')
        return JsonResponse(data=user_json,safe=False)
    except:
        return HttpResponse('NOT OK')
def wuliu_up_select(request):
    post_data = request.body
    post_data = json.loads(post_data)
    name=post_data.get('id')  #获得前段的用户编号字段
    user_json={}  #返回信息
    try:
        user_list=Wuliu.objects.filter(id=name).values()
        for user_i in user_list :
            user_json['id']=user_i.get('id')
            user_json['name']=user_i.get('name')
        return JsonResponse(data=user_json,safe=False)
    except:
        return HttpResponse('NOT OK')
def wenzi_up_select(request):
    post_data = request.body
    post_data = json.loads(post_data)
    name=post_data.get('id')  #获得前段的用户编号字段
    user_json={}  #返回信息
    try:
        user_list=Wenzi.objects.filter(id=name).values()
        for user_i in user_list :
            user_json['id']=user_i.get('id')
            user_json['name']=user_i.get('name')
        return JsonResponse(data=user_json,safe=False)
    except:
        return HttpResponse('NOT OK')
def wenzi_order_select(request):
    post_data = request.body
    post_data = json.loads(post_data)
    name=post_data.get('serch')  #获得前段的用户编号字段
    user_json=[]  #返回信息
    if name is None or name =='' :
        user_list = Wenzi.objects.all().values()
    else:
        user_list=Wenzi.objects.filter(Q(id__icontains=name)|Q(name__icontains=name)).values()
    for user_i in user_list :
        user_json.append(user_i)
    return JsonResponse(data=user_json,safe=False)
def style_order_select(request):
    post_data = request.body
    post_data = json.loads(post_data)
    name=post_data.get('serch')  #获得前段的用户编号字段
    user_json=[]  #返回信息
    if name is None or name =='' :
        user_list = Style.objects.all().values()
    else:
        user_list=Style.objects.filter(id=name).values()
    for user_i in user_list :
        user_json.append(user_i)
    return JsonResponse(data=user_json,safe=False)
def update_color(request):
    post_data = request.body
    post_data = json.loads(post_data).get('form_data')
    Color.objects.filter(color_id=post_data.get('color_id')).update(color_name=post_data.get('color_name'))
    return HttpResponse('OK')
def update_size(request):
    post_data = request.body
    post_data = json.loads(post_data).get('form_data')
    Size.objects.filter(size_id=post_data.get('size_id')).update(size_name=post_data.get('size_name'))
    return HttpResponse('OK')

def update_style(request):
    post_data = request.body
    post_data = json.loads(post_data).get('form_data')
    Style.objects.filter(id=post_data.get('id')).update(name=post_data.get('name'))
    return HttpResponse('OK')
def update_packing(request):
    post_data = request.body
    post_data = json.loads(post_data).get('form_data')
    Pack_method.objects.filter(id=post_data.get('id')).update(name=post_data.get('name'))
    return HttpResponse('OK')
def update_wuliu(request):
    post_data = request.body
    post_data = json.loads(post_data).get('form_data')
    Wuliu.objects.filter(id=post_data.get('id')).update(name=post_data.get('name'))
    return HttpResponse('OK')
def update_wenzi(request):
    post_data = request.body
    post_data = json.loads(post_data).get('form_data')
    Wenzi.objects.filter(id=post_data.get('id')).update(name=post_data.get('name'))
    return HttpResponse('OK')
def delete_color(request): #删除用户
    post_data = request.body
    name = json.loads(post_data).get('color_id')
    try:
        Color.objects.filter(color_id=name).delete()
        return HttpResponse('OK')
    except:
        return HttpResponse('NOT OK')
def delete_size(request): #删除用户
    post_data = request.body
    name = json.loads(post_data).get('color_id')
    try:
        Size.objects.filter(size_id=name).delete()
        return HttpResponse('OK')
    except:
        return HttpResponse('NOT OK')
def delete_style(request): #删除用户
    post_data = request.body
    name = json.loads(post_data).get('color_id')
    try:
        Style.objects.filter(id=name).delete()
        return HttpResponse('OK')
    except:
        return HttpResponse('NOT OK')
def delete_packing(request): #删除用户
    post_data = request.body
    name = json.loads(post_data).get('color_id')
    try:
        Pack_method.objects.filter(id=name).delete()
        return HttpResponse('OK')
    except:
        return HttpResponse('NOT OK')
def delete_wuliu(request): #删除用户
    post_data = request.body
    name = json.loads(post_data).get('id')
    try:
        Wuliu.objects.filter(id=name).delete()
        return HttpResponse('OK')
    except:
        return HttpResponse('NOT OK')
def delete_wenzi(request): #删除用户
    post_data = request.body
    name = json.loads(post_data).get('id')
    try:
        Wenzi.objects.filter(id=name).delete()
        return HttpResponse('OK')
    except:
        return HttpResponse('NOT OK')
def skutype(request):
    color_list=SkuType.objects.all().values()   #获得全部信息
    color_json = []
    for color_i in color_list:
        color_json.append(color_i)
    print(color_json)
    return JsonResponse(data=color_json,safe=False)
def add_skutype(request):
    post_data=request.body
    post_data=json.loads(post_data).get('form_data')
    #print(post_data)
    try:
        color_add=SkuType(id=post_data.get('id'),name=post_data.get('name'))
        color_add.save()
        return HttpResponse('OK')
    except:
        return HttpResponse('NOT OK')
def skutype_select(request):
    post_data = request.body
    post_data = json.loads(post_data)
    name=post_data.get('id')  #获得前段的用户编号字段
    user_json={}  #返回信息
    try:
        user_list=SkuType.objects.filter(id=name).values()
        for user_i in user_list :
            user_json['id']=user_i.get('id')
            user_json['name']=user_i.get('name')
        print(user_list)
        return JsonResponse(data=user_json,safe=False)
    except:
        return HttpResponse('NOT OK')

def update_skutype(request):
    post_data = request.body
    post_data = json.loads(post_data).get('form_data')
    SkuType.objects.filter(id=post_data.get('id')).update(name=post_data.get('name'))
    return HttpResponse('OK')
def delete_skutype(request): #删除分类
    post_data = request.body
    name = json.loads(post_data).get('id')
    try:
        SkuType.objects.filter(id=name).delete()
        return HttpResponse('OK')
    except:
        return HttpResponse('NOT OK')
def sku(request):    #获取sku信息
    post_data = request.body
    post_data = json.loads(post_data)
    print(post_data)
    user_json = []
    user_data={}
    if post_data.get('serch') == '' or post_data.get('serch') is None:
        user_list=SKU.objects.all().values()
    else:
        user_list = SKU.objects.filter(Q(id__icontains=post_data.get('serch'))|Q(name__icontains=post_data.get('serch'))).values()
    user_page=Paginator(user_list,post_data.get('size')).page(post_data.get('page'))
    total= Paginator(user_list,post_data.get('size')).count    #总计的数量
    for user_i in user_page:
        user_json.append(user_i)
    user_data['sku_list']=user_json
    user_data['total']=total
    return JsonResponse(data=user_data,safe=False)
def order_sku(request):    #获取sku信息
    post_data = request.body
    post_data = json.loads(post_data)
    user_json = []
    if post_data.get('serch'):
        user_list = SKU.objects.filter(Q(id__icontains=post_data.get('serch'))|Q(name__icontains=post_data.get('serch'))|Q(type__icontains=post_data.get('serch'))).values()
    else:
        user_list = SKU.objects.all().values()
    user_page = Paginator(user_list, 30).page(1)
    for user_i in user_page:
        user_json.append(user_i)
    return JsonResponse(data=user_json,safe=False)
def cl_order_sku(request):    #获取材料sku信息
    post_data = request.body
    post_data = json.loads(post_data)
    user_json = []
    if post_data.get('serch'):
        user_list = cl_SKU.objects.filter(Q(status=True),Q(id__icontains=post_data.get('serch'))|Q(name__icontains=post_data.get('serch'))|Q(type__icontains=post_data.get('serch'))).values()
    else:
        user_list = cl_SKU\
            .objects.filter(status=True).values()
    user_page = Paginator(user_list, 10).page(1)
    for user_i in user_page:
        user_json.append(user_i)
    return JsonResponse(data=user_json,safe=False)
def wuliu_order_select(request):
    post_data = request.body
    post_data = json.loads(post_data)
    user_json = []
    if post_data.get('serch') == '' or post_data.get('serch') is None:
        user_list = Wuliu.objects.all().values()
    else:
        user_list = Wuliu.objects.filter(Q(id__icontains=post_data.get('serch'))|Q(name__icontains=post_data.get('serch'))).values()
    for user_i in user_list:
        user_json.append(user_i)
    return JsonResponse(data=user_json,safe=False)
def size_order_select(request):   #选中链长的档案
    post_data = request.body
    post_data = json.loads(post_data)
    user_json = []
    if post_data.get('serch') == '' or post_data.get('serch') is None:
        user_list = Size.objects.all().values()
    else:
        user_list = Size.objects.filter(Q(size_name__icontains=post_data.get('serch'))).values()
    for user_i in user_list:
        user_json.append(user_i)
    return JsonResponse(data=user_json,safe=False)
def pur_order_select(request):  #选中供应商信息的列表
    post_data = request.body
    post_data = json.loads(post_data)
    user_json = []
    if post_data.get('serch') == '' or post_data.get('serch') is None:
        user_list = Contacts.objects.filter(status=True).values() #启用状态下的信息才能使用
    else:
        user_list = Contacts.objects.filter(Q(status=True),Q(id__icontains=post_data.get('serch'))|Q(name__icontains=post_data.get('serch'))).values()
    for user_i in user_list:
        user_json.append(user_i)
    return JsonResponse(data=user_json,safe=False)
def packing_order_select(request):
    post_data = request.body
    post_data = json.loads(post_data)
    user_json = []
    if post_data.get('serch') == '' or post_data.get('serch') is None:
        user_list = Pack_method.objects.all().values().order_by('-id')
    else:
        user_list = Pack_method.objects.filter(Q(id__icontains=post_data.get('serch'))|Q(name__icontains=post_data.get('serch'))).values().order_by('-id')
    for user_i in user_list:
        user_json.append(user_i)
    return JsonResponse(data=user_json,safe=False)
def sku_status(request):
    post_data = request.body
    post_data = json.loads(post_data)
    try:
        user_updade=SKU.objects.filter(id=post_data.get('name')).update(status=post_data.get('status_c'))
        return HttpResponse('OK')
    except:
        return HttpResponse('NOT OK')
def contacts_status(request):
    post_data = request.body
    post_data = json.loads(post_data)
    try:
        user_updade=Contacts.objects.filter(id=post_data.get('name')).update(status=post_data.get('status_c'))
        return HttpResponse('OK')
    except:
        return HttpResponse('NOT OK')
def cl_sku_status(request):
    post_data = request.body
    post_data = json.loads(post_data)
    try:
        user_updade=cl_SKU.objects.filter(id=post_data.get('name')).update(status=post_data.get('status_c'))
        return HttpResponse('OK')
    except:
        return HttpResponse('NOT OK')
def sku_up_select(request):
    post_data = request.body
    post_data = json.loads(post_data)
    name=post_data.get('id')  #获得前段的用户编号字段
    user_json={}  #返回信息
    try:
        user_list=SKU.objects.filter(id=name).values()
        for user_i in user_list :
            user_json['id']=user_i.get('id')
            user_json['name']=user_i.get('name')
            user_json['type']=user_i.get('type')
            user_json['unit']=user_i.get('unit')
            user_json['barcode']=user_i.get('barcode')
            user_json['price']=user_i.get('price')
            user_json['draw_price']=user_i.get('draw_price')
            user_json['style_num']=user_i.get('style_num')
            user_json['cost_price']=user_i.get('cost_price')
            user_json['imageUrl']=user_i.get('imageUrl')
        return JsonResponse(data=user_json,safe=False)
    except:
        return HttpResponse('NOT OK')
def sku_update(request):
    post_data = request.body
    post_data = json.loads(post_data).get('data')
    print(post_data)
    #try:
    SKU.objects.filter(id=post_data.get('id')).update(name=post_data.get('name'),type=post_data.get('type'),unit=post_data.get('unit'),barcode=post_data.get('barcode'),imageUrl=post_data.get('imageUrl'),
                                                      price=post_data.get('price'),draw_price=post_data.get('draw_price'),cost_price=post_data.get('cost_price'),style_num=post_data.get('style_num'))
    return HttpResponse('OK')
    #except:
        #return HttpResponse('NOT OK')
def contacts_update(request):
    post_data = request.body
    post_data = json.loads(post_data).get('data')
    Contacts.objects.filter(id=post_data.get('id')).update(name=post_data.get('name'),people=post_data.get('people'),phone=post_data.get('phone'),address=post_data.get('address'),note=post_data.get('note'))
    return HttpResponse('OK')
def cl_sku_update(request):
    post_data = request.body
    post_data = json.loads(post_data).get('data')
    cl_SKU.objects.filter(id=post_data.get('id')).update(name=post_data.get('name'),format=post_data.get('format'),unit=post_data.get('unit'),note=post_data.get('note'),
                                                         price=post_data.get('price'))
    return HttpResponse('OK')
def type_select(request):     #搜索框加载类别
    post_data = request.body
    type = json.loads(post_data).get('type')
    if type == '' or type is None :
        type_result=SkuType.objects.all().values()
        dict =[]
        dist={}
        for type_i in type_result:
            dist['type']=type_i.get('name')
            dict.append(dist)
            dist = {}
        return JsonResponse(data=dict, safe=False)
    else:
        type_result = SkuType.objects.filter(Q(name__icontains=type)).values()
        dict = []
        dist = {}
        for type_i in type_result:
            dist['type'] = type_i.get('name')
            dict.append(dist)
            dist = {}
        return JsonResponse(data=dict, safe=False)
def style_select(request):     #搜索框加载类别
    post_data = request.body
    type = json.loads(post_data).get('type')
    if type == '' or type is None :
        type_result=Style.objects.all().values()
        dict =[]
        dist={}
        for type_i in type_result:
            dist['type']=type_i.get('name')
            dict.append(dist)
            dist = {}
        return JsonResponse(data=dict, safe=False)
    else:
        type_result = Style.objects.filter(Q(name__icontains=type)).values()
        dict = []
        dist = {}
        for type_i in type_result:
            dist['type'] = type_i.get('name')
            dict.append(dist)
            dist = {}
        return JsonResponse(data=dict, safe=False)
def add_sku(request):
    date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))  # 获取当前时间
    post_data=request.body
    create_people = json.loads(post_data).get('create_people')
    post_data=json.loads(post_data).get('form_data')

    #print(post_data)
    try:
        user_add=SKU(id=post_data.get('id'),name=post_data.get('name'),type=post_data.get('type'),unit=post_data.get('unit'),barcode=post_data.get('barcode'),people=create_people,create_date=date,imageUrl=post_data.get('imageUrl'),
                     price=post_data.get('price'),draw_price=post_data.get('draw_price'),cost_price=post_data.get('cost_price'),style_num=post_data.get('style_num'))
        user_add.save()
        return HttpResponse('OK')
    except:
        return HttpResponse('NOT OK')
def add_cl_sku(request):
    date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))  # 获取当前时间
    post_data=request.body
    create_people = json.loads(post_data).get('create_people')
    post_data=json.loads(post_data).get('form_data')
    try:
        user_add=cl_SKU(id=post_data.get('id'),name=post_data.get('name'),format=post_data.get('format'),unit=post_data.get('unit'),note=post_data.get('note'),create_date=date,
                     create_user=create_people,price=post_data.get('price'))
        user_add.save()
        return HttpResponse('OK')
    except:
        return HttpResponse('NOT OK')
def add_contacts(request):   #增加材料信息
    date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))  # 获取当前时间
    post_data=request.body
    create_people = json.loads(post_data).get('create_people')
    post_data=json.loads(post_data).get('form_data')

    #print(post_data)
    try:
        user_add=Contacts(id=post_data.get('id'),name=post_data.get('name'),people=post_data.get('people'),phone=post_data.get('phone'),address=post_data.get('address'),note=post_data.get('note'),create_date=date,
                     create_user=create_people)
        user_add.save()
        return HttpResponse('OK')
    except:
        return HttpResponse('NOT OK')
def delete_sku(request): #删除用户
    post_data = request.body
    name = json.loads(post_data).get('name')
    try:
        SKU.objects.filter(id=name).delete()
        return HttpResponse('OK')
    except:
        return HttpResponse('NOT OK')
def delete_contacts(request): #删除往来对象
    post_data = request.body
    name = json.loads(post_data).get('name')
    try:
        Contacts.objects.filter(id=name).delete()
        return HttpResponse('OK')
    except:
        return HttpResponse('NOT OK')
def delete_cl_sku(request): #删除往来对象
    post_data = request.body
    name = json.loads(post_data).get('name')
    try:
        cl_SKU.objects.filter(id=name).delete()
        return HttpResponse('OK')
    except:
        return HttpResponse('NOT OK')
def wuliu(request):
    color_list = Wuliu.objects.all().values()  # 获得全部信息
    color_json = []
    for color_i in color_list:
        color_json.append(color_i)
    return JsonResponse(data=color_json, safe=False)
def wenzi(request):
    color_list = Wenzi.objects.all().values()  # 获得全部信息
    color_json = []
    for color_i in color_list:
        color_json.append(color_i)
    return JsonResponse(data=color_json, safe=False)
def img(request):  #SKU上传
    # 获取文件
    if request.method=='GET':
        md5 = request.GET.get("md5")
        imgfile = os.path.join(MEDIA_ROOT,md5 + '.jpg').replace('\\', '/')
        imgfile=imgfile.replace('"','')
        if os.path.exists(imgfile):
            data = open(imgfile, 'rb').read()
            return FileResponse(open(imgfile, "rb"), content_type="image/jpg")
        else: #检索不到jpg格式时
            imgfile = os.path.join(MEDIA_ROOT, md5 + '.jpeg').replace('\\', '/')
            imgfile = imgfile.replace('"', '')
            if os.path.exists(imgfile):
                data = open(imgfile, 'rb').read()
                return FileResponse(open(imgfile, "rb"), content_type="image/jpeg")
            else: #标识jpeg格式也没有找到
                imgfile = os.path.join(MEDIA_ROOT,md5 + '.png').replace('\\', '/')
                imgfile = imgfile.replace('"', '')
                if os.path.exists(imgfile):
                    data = open(imgfile, 'rb').read()
                    return FileResponse(open(imgfile, "rb"), content_type="image/png")
    if request.method=='POST':
        files = request.FILES
        response = []
        # 取出文件的 key 和 value
        for key, value in files.items():
            # 读取文件
            content = value.read()
            md5 = hashlib.md5(content).hexdigest()
            # 指定文件路径
            path = os.path.join(MEDIA_ROOT, md5 + '.jpg')

            with open(path, 'wb') as f:
                # 保存文件
                f.write(content)
        return JsonResponse(data=md5, safe=False)
def img_order(request):  #获取订单图片
    # 获取文件
    if request.method=='GET':
        md5 = request.GET.get("md5")
        imgfile = os.path.join(MEDIA_ROOT,'order/',md5 + '.jpg').replace('\\', '/')
        imgfile=imgfile.replace('"','')
        if os.path.exists(imgfile):
            data = open(imgfile, 'rb').read()
            return FileResponse(open(imgfile, "rb"), content_type="image/jpg")
        else: #检索不到jpg格式时
            imgfile = os.path.join(MEDIA_ROOT,'order/', md5 + '.jpeg').replace('\\', '/')
            imgfile = imgfile.replace('"', '')
            if os.path.exists(imgfile):
                data = open(imgfile, 'rb').read()
                return FileResponse(open(imgfile, "rb"), content_type="image/jpeg")
            else: #标识jpeg格式也没有找到
                imgfile = os.path.join(MEDIA_ROOT,'order/',md5 + '.png').replace('\\', '/')
                imgfile = imgfile.replace('"', '')
                if os.path.exists(imgfile):
                    data = open(imgfile, 'rb').read()
                    return FileResponse(open(imgfile, "rb"), content_type="image/png")
    if request.method=='POST':
        files = request.FILES
        response = []
        # 取出文件的 key 和 value
        for key, value in files.items():
            # 读取文件
            content = value.read()
            md5 = hashlib.md5(content).hexdigest()
            # 指定文件路径
            path = os.path.join(MEDIA_ROOT,'order/', md5 + '.jpg')

            with open(path, 'wb') as f:
                # 保存文件
                f.write(content)
        return JsonResponse(data=md5, safe=False)
def delete_img(request):   #删除图片
    md5 = request.GET.get('md5')
    img_name = md5 + '.jpg'
    path = os.path.join(MEDIA_ROOT, img_name).replace('\\', '/')
    path = path.replace('"', '')
    print(path)
    if os.path.exists(path):
        os.remove(path)
        return JsonResponse(data='OK', safe=False)
    else:
        return JsonResponse(data='NOT OK', safe=False)
def cop_order(request):    #抓取客户单号
    chache=pysql("exec PROC_NumIndent ")
    pysql_update("insert into num VALUES ('{}')".format(chache[0][0]))    #单号插入记录表
    return JsonResponse(data=chache, safe=False)
def pur_order(request):    #抓取入库单号
    chache=pysql("exec PROC_NumIndent_PUR ")
    pysql_update("insert into pur_num VALUES ('{}')".format(chache[0][0]))    #单号插入记录表
    return JsonResponse(data=chache, safe=False)
def cop_order_excel():    #抓取客户单号
    chache=pysql("exec PROC_NumIndent ")
    pysql_update("insert into num VALUES ('{}')".format(chache[0][0]))    #单号插入记录表
    return chache[0][0]
def order_save(request):
    date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))  # 获取当前时间
    post_data=request.body  #获得页面数据
    post_data=json.loads(post_data)
    print(post_data)
    order_tou=post_data.get('order_tou')
    order_shen=post_data.get('order_shen')
    if order_tou.get('add') == '选项1' :
        add='义乌'
    else:
        add='杭州'
    #1.先删除内容,主动存在保存
    Order.objects.filter(id=order_tou.get('order_code')).delete()  #删除单头
    Order_Del.objects.filter(order_key=order_tou.get('order_code')).delete() #删除单身
    amount = 0 #金额汇总
    order_shen_list=[]
    for order_i in order_shen:
        order_shen_i=Order_Del(order_key=order_tou.get('order_code'),order_code=order_i.get('order_code'),item_code=order_i.get('item_code'),item_name=order_i.get('item_name'),order_name=order_i.get('order_name'),
                                  unit=order_i.get('unit'),skutype=order_i.get('skutype'),color=order_i.get('color'),words=order_i.get('words'),num=order_i.get('num'),draw_price=order_i.get('draw_price'),style_num=order_i.get('style_num'),
                                  wuliu=order_i.get('wuliu'),pack_method=order_i.get('pack_method'),note=order_i.get('note'),size=order_i.get('size'),total_num=order_i.get('total_num'),draw_amount=order_i.get('draw_amount'),
                                  create_date=order_i.get('create_date'),end_date=order_i.get('end_date'),state='未审核',order_type=order_i.get('order_type'),sku_style=order_i.get('sku_style'),
                                  order_level=order_i.get('order_level'),amount=order_i.get('amount'),order_img=order_i.get('order_img'),picture=order_i.get('picture'),salesman=order_tou.get('saleman'),date=order_tou.get('date'))
        order_level= order_i.get('order_level')
        order_shen_list.append(order_shen_i)
        amount = amount +float(order_i.get('amount'))
        amount = round(amount,2)
    Order_Del.objects.bulk_create(order_shen_list)  #单身批量保存
    order_tou_save = Order(id=order_tou.get('order_code'), date=order_tou.get('date'), add=add,total_amount=amount,
                           note=order_tou.get('note'), salesman=order_tou.get('saleman'), create_time=date,
                           create_user=order_tou.get('create_user'), total_num=order_tou.get('total_num'),order_level=order_level,draw_status='未画图')
    order_tou_save.save()
    order_level = order_i.get('order_level')
    return HttpResponse('OK')
def cl_order_save(request):
    date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))  # 获取当前时间
    post_data=request.body  #获得页面数据
    post_data=json.loads(post_data)
    print(post_data)
    order_tou=post_data.get('order_tou')
    order_shen=post_data.get('order_shen')

    order_tou_save=Warehousing(id=order_tou.get('order_code'),date=order_tou.get('date'),note=order_tou.get('note'),supplier_ware=order_tou.get('supplier_ware'),create_time=date,create_user=order_tou.get('create_user'))

    for order_i in order_shen:
        order_shen_save=Warehous_Del(order_key=order_tou.get('order_code'),item_code=order_i.get('item_code'),item_name=order_i.get('item_name'),format=order_i.get('format'),
                                  unit=order_i.get('unit'),num=order_i.get('num'),price=order_i.get('price'),total=order_i.get('total'),note=order_i.get('note'),
                                  supplier_ware=order_tou.get('supplier_ware'),create_user=order_tou.get('create_user'),state='未审核',date=order_tou.get('date'))
        order_shen_save.save()
    order_tou_save.save()
    return HttpResponse('OK')
def cl_order_update(request):
    date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))  # 获取当前时间
    post_data=request.body  #获得页面数据
    post_data=json.loads(post_data)
    print(post_data)
    order_tou=post_data.get('order_tou')
    order_shen=post_data.get('order_shen')
    #1,先将之前的内容删除
    Warehousing.objects.filter(id=order_tou.get('id')).delete()
    Warehous_Del.objects.filter(order_key=order_tou.get('id')).delete()
    #2.重新保存内容
    order_tou_save=Warehousing(id=order_tou.get('id'),date=order_tou.get('date'),note=order_tou.get('note'),supplier_ware=order_tou.get('supplier_ware'),create_time=date,create_user=order_tou.get('create_user'),total_num=order_tou.get('total_num'))

    for order_i in order_shen:
        order_shen_save=Warehous_Del(order_key=order_tou.get('id'),item_code=order_i.get('item_code'),item_name=order_i.get('item_name'),format=order_i.get('format'),
                                  unit=order_i.get('unit'),num=order_i.get('num'),price=order_i.get('price'),total=order_i.get('total'),note=order_i.get('note'),
                                  supplier_ware=order_tou.get('supplier_ware'),create_user=order_tou.get('create_user'),state='未审核',date=order_tou.get('date'))
        order_shen_save.save()
    order_tou_save.save()
    return HttpResponse('OK')
def update_mima(request):
    post_data = request.body
    post_data = json.loads(post_data)
    print(post_data)
    mima_old=User.objects.filter(name=post_data.get('id'),password=post_data.get('password_old'))
    if mima_old:
        User.objects.filter(name=post_data.get('id'),password=post_data.get('password_old')).update(password=post_data.get('password_new'))
        return HttpResponse('OK')
    else:
        return HttpResponse('300')
def page_get(request):  #页面查询和修改初始化
    post_data = request.body  # 获得页面数据
    post_data = json.loads(post_data)
    order_num=post_data.get('order')   #得到单号
    order_tou=Order.objects.filter(id=order_num).values()
    order_tou=order_tou[0]
    order_shen=Order_Del.objects.filter(order_key=order_num).values()
    data={}
    data['tou']=order_tou
    data['shen']=list(order_shen)
    print(data)
    return JsonResponse(data=data, safe=False)
def pur_page_get(request):  #页面查询和修改初始化
    post_data = request.body  # 获得页面数据
    post_data = json.loads(post_data)
    order_num=post_data.get('order')   #得到单号
    order_tou=Warehousing.objects.filter(id=order_num).values()
    order_tou=order_tou[0]
    order_shen_json=[]
    order_shen=Warehous_Del.objects.filter(order_key=order_num).values()
    for order_shen_i in order_shen:
        order_shen_json.append(order_shen_i)
    data={}
    data['tou']=order_tou
    data['shen']=order_shen_json
    print(data)
    return JsonResponse(data=data, safe=False)
def order_update(request):
    date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))  # 获取当前时间
    post_data=request.body  #获得页面数据
    post_data=json.loads(post_data)
    order_tou=post_data.get('order_tou')
    user_name = post_data.get('user_name')  #用户名称
    print(user_name)
    order_shen=post_data.get('order_shen')
    order_delete=post_data.get('delete_li')   #记录删除的内容
    add_order=order_tou.get('add')
    if order_tou.get('add') == '选项1' :
        add_order='义乌'
    elif order_tou.get('add') == '选项2':
        add_order='杭州'

    #删除前台删除的内容
    Order_Del.objects.filter(order_key=order_tou.get('id')).delete()
    total_num = 0 #单头合计
    order_shen_list = []
    amount = 0
    order_level=''
    for order_i in order_shen:
        order_level = order_i.get('order_level')
        order_shen_i = Order_Del(order_key=order_tou.get('id'), order_code=order_i.get('order_code'),
                                    item_code=order_i.get('item_code'), item_name=order_i.get('item_name'),order_name=order_i.get('order_name'),
                                    unit=order_i.get('unit'), skutype=order_i.get('skutype'),
                                    color=order_i.get('color'), words=order_i.get('words'),
                                    draw_price=order_i.get('draw_price'),style_num=order_i.get('style_num'),draw_amount=order_i.get('draw_amount'),
                                    num=order_i.get('num'),sku_style=order_i.get('sku_style'),
                                    wuliu=order_i.get('wuliu'), lianchang=order_i.get('liangchang'),
                                    note=order_i.get('note'), size=order_i.get('size'),pack_method=order_i.get('pack_method'),
                                    total_num=order_i.get('total_num'),date=order_tou.get('date'),
                                    create_date=order_i.get('create_date'), end_date=order_i.get('end_date'),
                                    state='未审核',order_type=order_i.get('order_type'),salesman=order_tou.get('salesman'),
                                    order_level=order_i.get('order_level'),amount=order_i.get('amount'),order_img=order_i.get('order_img'),picture=order_i.get('picture'))
        order_shen_list.append(order_shen_i)
        total_num = total_num + int(order_i.get('num'))
        amount = amount +float(order_i.get('amount'))
        amount = round(amount,2)
    order_tou_save = Order.objects.filter(id=order_tou.get('id')).update(date=order_tou.get('date'), add=add_order,
                                                                         note=order_tou.get('note'),total_num = total_num,total_amount=amount,
                                                                         salesman=order_tou.get('salesman'),order_level=order_level,
                                                                         update_user=user_name, update_time=date)
    Order_Del.objects.bulk_create(order_shen_list)   #保存
    return HttpResponse('OK')

def test(request):
    return HttpResponse(path)
def delete_order(request):
    post_data=request.body  #获得页面数据
    post_data=json.loads(post_data)
    name=post_data.get('name')
    Order.objects.filter(id=name).delete()
    Order_Del.objects.filter(order_key=name).delete()
    return HttpResponse('OK')
def delete_ware(request):
    post_data=request.body  #获得页面数据
    post_data=json.loads(post_data)
    name=post_data.get('name')
    Warehousing.objects.filter(id=name).delete()
    Warehous_Del.objects.filter(order_key=name).delete()
    return HttpResponse('OK')
def order_Approval(request):
    date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))  # 获取当前时间
    post_data = request.body  # 获得页面数据
    post_data = json.loads(post_data)
    order_num=post_data.get('order')
    user=post_data.get('user')
    xiugai=Order.objects.filter(id=order_num).update(examine=user,examine_time=date,status='审核')
    Order_Del.objects.filter(order_key=order_num).update(state='审核')
    return HttpResponse('OK')
def order_Approval_cancel(request):
    post_data = request.body  # 获得页面数据
    post_data = json.loads(post_data)
    order_num=post_data.get('order')
    user=post_data.get('user')
    if Order_Del.objects.filter(order_key=order_num,draw_status__in= ['画图完成', '待拉图', '拉图完成']):  #标识已经有了或许的动作
        return HttpResponse(404) #标识已经存在了别的状态,不能撤销
    else:
        xiugai = Order.objects.filter(id=order_num).update(examine='', examine_time='',status='未审核')
        Order_Del.objects.filter(order_key=order_num).update(state='未审核')
        return HttpResponse('OK')
def pur_Approval(request):  #采购单审核
    date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))  # 获取当前时间
    post_data = request.body  # 获得页面数据
    post_data = json.loads(post_data)
    order_num=post_data.get('order')
    user=post_data.get('user')
    #1,读取单身所有的数据 2.将单身的数据更新到库存明细表中
    order_cl_del =Warehous_Del.objects.filter(order_key=order_num).values()
    for order_i in order_cl_del:
        if Stock.objects.filter(item_code=order_i.get('item_code')):    #标识改SKU已经存在了库存记录
            #1.直接更新库存就行了,首先获取库存
            num = Stock.objects.filter(item_code =order_i.get('item_code')).values()[0]
            Stock.objects.filter(item_code =order_i.get('item_code')).update(stock_num=num+order_i.get('num'))
        else: #标识库存明细里面没有这一行,增加行信息
            stock_save = Stock(item_code=order_i.get('item_code'),item_name=order_i.get('item_name'),format=order_i.get('format'),unit=order_i.get('unit'),stock_num=order_i.get('num'))
            stock_save.save()  #保存信息
    #更改原订单单头信息
    xiugai=Warehousing.objects.filter(id=order_num).update(examine=user,examine_time=date)
    Warehous_Del.objects.filter(order_key=order_num).update(state='审核')
    return HttpResponse('OK')
def order_del(request):
    post_data = request.body
    post_data = json.loads(post_data)
    user_json = []
    user_data = {}
    selectForm = post_data.get('serch')
    print(selectForm)
    if selectForm.get('date') or selectForm.get('order_code') or selectForm.get('draw_status') or selectForm.get('order_level') or selectForm.get('color') or selectForm.get('words')\
            or selectForm.get('type') or selectForm.get('order_name') or selectForm.get('salesman'):
        user_list=Order_Del.objects.all()
        if selectForm.get('date'):
            print(selectForm.get('date'))
        if selectForm.get('order_code'):
            user_list=user_list.filter(order_code__contains=selectForm.get('order_code'))
        if selectForm.get('draw_status'):
            user_list=user_list.filter(draw_status=selectForm.get('draw_status'))
        if selectForm.get('order_level'):
            user_list=user_list.filter(order_level=selectForm.get('order_level'))
        if selectForm.get('color'):
            user_list=user_list.filter(color=selectForm.get('color'))
        if selectForm.get('words'):
            user_list=user_list.filter(words=selectForm.get('words'))
        if selectForm.get('type'):
            user_list = user_list.filter(skutype=selectForm.get('type'))
        if selectForm.get('order_name'):
            user_list = user_list.filter(order_name__contains=selectForm.get('order_name'))
        if selectForm.get('salesman'):
            user_list = user_list.filter(salesman__contains=selectForm.get('salesman_code'))
        user_list=user_list.values().order_by('-id')   #转换取值

    else:
        user_list = Order_Del.objects.all().values().order_by('-id')
    user_page = Paginator(user_list, post_data.get('size')).page(post_data.get('page'))
    total = Paginator(user_list, post_data.get('size')).count  # 总计的数量
    for user_i in user_page:
        user_json.append(user_i)
    user_data['user_list'] = user_json
    user_data['total'] = total
    return JsonResponse(data=user_data, safe=False)
def order_del_picture(request):

    post_data = request.body  # 获得页面数据
    post_data = json.loads(post_data)
    order_num = post_data.get('serch')
    order_shen_json = []
    order_shen_jin = Order_Del.objects.filter(pi_code=order_num, color='金色')  # 获得本批次所有的订单
    order_shen_jin = order_shen_jin.exclude(state='关闭').values().order_by('order_name')
    for order_i_jin in order_shen_jin:
        order_shen_json.append(order_i_jin)

    order_shen_bai = Order_Del.objects.filter(pi_code=order_num, color='白金')  # 获得本批次所有的订单
    order_shen_bai = order_shen_bai.exclude(state='关闭').values().order_by('order_name')
    for order_i_bai in order_shen_bai:
        order_shen_json.append(order_i_bai)

    order_shen_mei = Order_Del.objects.filter(pi_code=order_num, color='玫瑰金')  # 获得本批次所有的订单
    order_shen_mei = order_shen_mei.exclude(state='关闭').values().order_by('order_name')
    for order_i_mei in order_shen_mei:
        order_shen_json.append(order_i_mei)

    order_shen_qita = Order_Del.objects.filter(pi_code=order_num)  # 获得本批次所有的订单
    order_shen_qita = order_shen_qita.exclude(color='金色')
    order_shen_qita = order_shen_qita.exclude(state='关闭')
    order_shen_qita = order_shen_qita.exclude(color='玫瑰金')
    order_shen_qita = order_shen_qita.exclude(color='白金').values().order_by('order_name')
    for order_i_qita in order_shen_qita:
        order_shen_json.append(order_i_qita)

    data = {}
    data['user_list'] = order_shen_json
    return JsonResponse(data=data, safe=False)

def order_del_draw(request):
    post_data = request.body
    post_data = json.loads(post_data)
    user_id= post_data.get('user')
    user_info = User.objects.filter(name=user_id).values()
    user_code = user_info[0].get('nameid')
    user_address = user_info[0].get('address')  # 获取地区
    user_radio = user_info[0].get('radio')  # 获取用户订单权限
    print(user_radio,user_address)
    user_json = []
    user_data = {}
    selectForm = post_data.get('serch')
    if user_radio == '3':  # 标识全部订单
        if selectForm.get('date') or selectForm.get('order_code') or selectForm.get('order_level') or selectForm.get('salesman'):
            user_list=Order.objects.filter(draw_status='未画图',status='审核')
            if selectForm.get('date'):
                print(selectForm.get('date'))
            if selectForm.get('order_code'):
                user_list=user_list.filter(id__contains=selectForm.get('order_code'))
            if selectForm.get('order_level'):
                user_list=user_list.filter(order_level=selectForm.get('order_level'))
            if selectForm.get('salesman'):
                user_list = user_list.filter(create_user__contains=selectForm.get('salesman_code'))
            user_list=user_list.values().order_by('-id')   #转换取值

        else:
            user_list = Order.objects.filter(draw_status='未画图',status='审核').values().order_by('-id')
    elif user_radio == '2':  # 标识本地区所有的订单:
        if selectForm.get('date') or selectForm.get('order_code') or selectForm.get('order_level')  or selectForm.get('salesman'):
            user_list = Order.objects.filter(add=user_address, draw_status='未画图',status='审核')
            if selectForm.get('date'):
                print(selectForm.get('date'))
            if selectForm.get('order_code'):
                user_list = user_list.filter(id__contains=selectForm.get('order_code'))
            if selectForm.get('order_level'):
                user_list = user_list.filter(order_level=selectForm.get('order_level'))
            if selectForm.get('salesman'):
                user_list = user_list.filter(create_user__contains=selectForm.get('salesman_code'))
            user_list = user_list.values().order_by('-id')  # 转换取值

        else:
            user_list = Order.objects.filter(draw_status='未画图',status='审核',add=user_address).values().order_by('-id')

    elif user_radio == '3':  # 标识自由自己的订单:
        if selectForm.get('date') or selectForm.get('order_code') or selectForm.get('order_level')  or selectForm.get('salesman'):
            user_list = Order.objects.filter(create_user=user_code, draw_status='未画图',status='审核')
            if selectForm.get('date'):
                print(selectForm.get('date'))
            if selectForm.get('order_code'):
                user_list = user_list.filter(id__contains=selectForm.get('order_code'))
            if selectForm.get('order_level'):
                user_list = user_list.filter(order_level=selectForm.get('order_level'))
            if selectForm.get('salesman'):
                user_list = user_list.filter(create_user__contains=selectForm.get('salesman_code'))
            user_list = user_list.values().order_by('-id')  # 转换取值

        else:
            user_list = Order.objects.filter(draw_status='未画图',status='审核',create_user=user_code).values().order_by('-id')

    user_page = Paginator(user_list, post_data.get('size')).page(post_data.get('page'))
    total = Paginator(user_list, post_data.get('size')).count  # 总计的数量
    for user_i in user_page:
        user_json.append(user_i)
    user_data['user_list'] = user_json
    user_data['total'] = total
    return JsonResponse(data=user_data, safe=False)
def draw_save(request):
    post_data = request.body
    post_data = json.loads(post_data)
    data=post_data.get('data')
    print(data)
    Order_Del.objects.filter(id=data.get('id')).update(draw_img=data.get('imgurl'),draw_status='画图完成')
    return HttpResponse(200)
def saleman(request):    #获取所有的人员信息
    post_data = request.body
    post_data = json.loads(post_data)
    user_json = []
    if post_data.get('serch'):
        user_list = User.objects.filter(Q(name__icontains=post_data.get('serch'))|Q(nameid__icontains=post_data.get('serch'))).values('name','nameid')
    else:
        user_list = User.objects.all().values('name','nameid')

    #user_page = Paginator(user_list, 10).page(1)
    for user_i in user_list:
        user_json.append(user_i)
    return JsonResponse(data=user_json,safe=False)
def packing_save(request):
    date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))  # 获取当前时间
    post_data = request.body
    post_data = json.loads(post_data)
    order_id=post_data.get('order_id')
    user_code=post_data.get('user_code')
    if Order_Del.objects.filter(id=order_id): #如果存在表示扫描正确
        order_del=Order_Del.objects.filter(id=order_id).values('state','num','packing_num','order_code','order_name','item_code','item_name','total_num','wuliu','color','words','lianchang')
        order_del=order_del[0]
        num = order_del.get('num')
        packing_num = order_del.get('packing_num')
        if order_del.get('packing_num') == '已关闭':
            return HttpResponse(405)  # 订单已关闭
        if packing_num < num :  #包装数量小于订单数量
            price=SKU.objects.filter(id=order_del.get('item_code')).values('price')[0].get('price')   #获得单价信息
            pack=packing(order_key=order_id,user_code=user_code,date=date,order_code=order_del.get('order_code'),name=order_del.get('order_name'),item_code=order_del.get('item_code'),
                         item_name=order_del.get('item_name'),total_num=order_del.get('total_num'),packing_num=1,wuliu=order_del.get('wuliu'),color=order_del.get('color'),
                         words=order_del.get('words'),lianchang=order_del.get('lianchang'),price=price)
            pack.save()  #保存

            Order_Del.objects.filter(id=order_id).update(packing_num=packing_num+1,page_status='已包装')  #数量加一
            return JsonResponse(data=order_del, safe=False)
        else:
            return HttpResponse(403) #数量已经满足了,不能重复
    else: #扫描错误
        return HttpResponse(404)
def packing_list(request):    #获取sku信息
    post_data = request.body
    post_data = json.loads(post_data)
    user_json = []
    user_data={}
    user_list = packing.objects.filter(user_code=post_data.get('user_code')).values().order_by('-id')
    user_page=Paginator(user_list,post_data.get('size')).page(post_data.get('page'))
    total= Paginator(user_list,post_data.get('size')).count    #总计的数量
    for user_i in user_page:
        user_json.append(user_i)
    user_data['packing_li']=user_json
    user_data['total']=total
    return JsonResponse(data=user_data,safe=False)
def packing_list_all(request):    #所有的包装信息
    post_data = request.body
    post_data = json.loads(post_data)
    user_json = []
    user_data={}
    user_list = packing.objects.all().values().order_by('-id')
    user_page=Paginator(user_list,post_data.get('size')).page(post_data.get('page'))
    total= Paginator(user_list,post_data.get('size')).count    #总计的数量
    for user_i in user_page:
        user_json.append(user_i)
    user_data['packing_li']=user_json
    user_data['total']=total
    return JsonResponse(data=user_data,safe=False)
def order_out_one(request):
    post_data = request.body
    post_data = json.loads(post_data)
    order = post_data.get('order') #得到订单号
    if Order_Del.objects.filter(order_code=order): #如果订单号存在
        Order_Del.objects.filter(order_code=order).update(chuku_status='已出库')
        return HttpResponse('OK')
    else: #订单号不存在
        return HttpResponse(404)
def packing_pl(request):
    post_data = request.body
    post_data = json.loads(post_data)
    order_pl= post_data.get('data')
    order_pl=order_pl.split('\n')
    for order_i in order_pl:
        if Order_Del.objects.filter(order_code=order_i):
            Order_Del.objects.filter(order_code=order_i).update(chuku_status='已出库')
            return HttpResponse('OK')
        else:#表示订单号不存在
            return HttpResponse(order_i)
def roles(request): #一级菜单
    role=Roles.objects.all().values()
    role_json = []
    for role_i in role:
        role_json.append(role_i)
    return JsonResponse(data=role_json,safe=False)
def quanxian_list_all(request):    #三级菜单
    quanxian_list=quanxian.objects.all().values().order_by('sort')
    quanxian_json = []
    for quanxian_i in quanxian_list:
        quanxian_json.append(quanxian_i)
    dict = {}
    list = []  # 最终结果集合
    chiid_dict={}  #子菜单
    chiid_list=[]  #子菜单

    button_dict = {}  # 三级子菜单
    button_list = []  # 三级子菜单

    for quanxian_j in quanxian_json:
        #print(quanxian_j)
        if quanxian_j.get('level') == '0':  #一级菜单
            dict['id']=quanxian_j.get('jon_code')
            dict['name']=quanxian_j.get('job_name')
            for quanxian_h in quanxian_json:
                if int(quanxian_h.get('jon_code')[0]) == int(quanxian_j.get('jon_code')) and quanxian_h.get('jon_code') != quanxian_j.get('jon_code') and quanxian_h.get('level') == '1':
                    chiid_dict['id']=quanxian_h.get('jon_code')
                    chiid_dict['name']=quanxian_h.get('job_name')
                    for quanxian_b in quanxian_json:
                        if quanxian_b.get('code_name') == quanxian_h.get('jon_code') and quanxian_b.get('level') == '2':
                            button_dict['id'] = quanxian_b.get('jon_code')
                            button_dict['name'] = quanxian_b.get('job_name')
                            button_list.append(button_dict)  #集合三级菜单
                            button_dict={}  #清空按钮
                    chiid_dict['children']=button_list
                    button_list=[]  #清空三级节点
                    chiid_list.append(chiid_dict)   #完成子集合
                    chiid_dict={}  #完成清空
            dict['children']=chiid_list
            chiid_list=[]   #完成清空
            list.append(dict)
            dict={}    #清空结果集合
    return JsonResponse(data=list,safe=False)

def role_check(request):
    post_data = request.body
    post_data = json.loads(post_data)
    role_name=post_data.get('role') #得到角色的名称
    role_check_all = Roles_Del.objects.filter(role_name=role_name,level='2').values('jon_code') #获得本角色的所有内容

    role_list=[]
    for role_i in role_check_all:
        role_list.append(role_i.get('jon_code'))
    return JsonResponse(data=role_list, safe=False)
def role_save(request):
    post_data = request.body
    post_data = json.loads(post_data)
    role_name = post_data.get('role')  # 得到角色的名称
    keys = post_data.get('keys')  # 得到具体的角色列表
    #执行第一步将目前该角色的所有权限清空
    Roles_Del.objects.filter(role_name=role_name).delete()
    #执行第二部,清空之后重新新增
    for key_i in keys:
        roles_save=Roles_Del(role_name=role_name,jon_code=key_i)
        roles_save.save()
    #更新额外字段到角色表
    pysql_update("update kaijaing_roles_del set code_name=B.code_name,job_name=B.job_name,level=B.level,sort=B.sort from kaijaing_roles_del A inner join kaijaing_quanxian B on A.jon_code = B.jon_code where A.role_name = '{}'".
                 format(role_name))
    return HttpResponse('OK')
def role_new(request):
    post_data = request.body
    post_data = json.loads(post_data)
    data = post_data.get('form_data')  # 得到角色的名称
    name=data.get('name')
    name_del=data.get('name_del')
    if Roles.objects.filter(role_name=name):
        return HttpResponse('cuzai')
    else:
        role=Roles(role_name=name,role_explain=name_del)
        role.save()
        return HttpResponse('OK')
def role_select(request):
    post_data = request.body
    post_data = json.loads(post_data)
    name=post_data.get('role')  #获得前段的用户编号字段
    user_json=[]  #返回信息
    if name:
        user_list=Roles.objects.filter(role_name__icontains=name).values('role_name')
    else:
        user_list = Roles.objects.all().values('role_name')
    for user_i in user_list:
        user_json.append(user_i)
    print(user_json)
    return JsonResponse(data=user_json,safe=False)
def update_role_select(request):
    post_data = request.body
    post_data = json.loads(post_data)
    name = post_data.get('name')  # 获得前段的用户编号字段
    roles_get = Roles.objects.filter(role_name=name).values()
    user_json={}
    for user_i in roles_get:
        user_json['name'] = user_i.get('role_name')
        user_json['name_del'] = user_i.get('role_explain')
    return JsonResponse(data=user_json, safe=False)
def role_up_save(request):
    post_data = request.body
    post_data = json.loads(post_data)
    upform = post_data.get('upform')  # 获得前段的用户编号字段
    Roles.objects.filter(role_name=upform.get('name')).update(role_explain=upform.get('name_del'))
    return HttpResponse('OK')
def delete_role(request):
    post_data = request.body
    post_data = json.loads(post_data)
    role_name = post_data.get('role_name')  # 获得前段的用户编号字段
    Roles.objects.filter(role_name=role_name).delete()
    Roles_Del.objects.filter(role_name=role_name).delete()
    return HttpResponse('OK')
def get_user_name(request):
    post_data = request.body
    post_data = json.loads(post_data)
    user_code = post_data.get('user_name')  #获得用户编号
    user_names = User.objects.filter(name=user_code).values('nameid')  #获得用户名
    print(user_code,user_names)
    user_name = user_names[0].get('nameid')
    return JsonResponse(data=user_name,safe=False)
def get_role(request):
    post_data = request.body
    post_data = json.loads(post_data)
    name = post_data.get('user_name')  #得到用户账号
    #print(name)
    if name :
        role = User.objects.filter(name=name).values('role')  # 获得角色名称

        role_name = post_data.get('role')  # 得到角色的名称
        role_check_all = Roles_Del.objects.filter(role_name=role[0].get('role'), level='2').values('jon_code')  # 获得本角色的所有内容

        role_list = []
        for role_i in role_check_all:
            role_list.append(role_i.get('jon_code'))
        #print(role_list)
        return JsonResponse(data=role_list, safe=False)
def store_excel(request):  #订单导入模板
    md5 ='order'
    imgfile = os.path.join(MEDIA_ROOT, md5 + '.xls').replace('\\', '/')
    imgfile = imgfile.replace('"', '')
    if os.path.exists(imgfile):
        data = open(imgfile, 'rb').read()

        # update_file_path文件存放位置
        file = open(imgfile, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/vnd.ms-excel'
        # file_name下载下来保存的文件名字
        response['Content-Disposition'] = f"attachment; filename={escape_uri_path('订单导入模板.xls')};"
        return response
def install_lodop32(request):  #订单导入模板
    md5 ='install_lodop32'
    imgfile = os.path.join(MEDIA_ROOT, md5 + '.exe').replace('\\', '/')
    imgfile = imgfile.replace('"', '')
    if os.path.exists(imgfile):
        data = open(imgfile, 'rb').read()

        # update_file_path文件存放位置
        file = open(imgfile, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/x-msdownload'
        # file_name下载下来保存的文件名字
        response['Content-Disposition'] = f"attachment; filename={escape_uri_path('install_lodop32.exe')};"
        return response
def install_lodop64(request):  #订单导入模板
    md5 ='install_lodop64'
    imgfile = os.path.join(MEDIA_ROOT, md5 + '.exe').replace('\\', '/')
    imgfile = imgfile.replace('"', '')
    if os.path.exists(imgfile):
        data = open(imgfile, 'rb').read()

        # update_file_path文件存放位置
        file = open(imgfile, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/x-msdownload'
        # file_name下载下来保存的文件名字
        response['Content-Disposition'] = f"attachment; filename={escape_uri_path('install_lodop64.exe')};"
        return response
def CLodop_Setup_for_Win32NT(request):  #订单导入模板
    md5 ='CLodop_Setup_for_Win32NT'
    imgfile = os.path.join(MEDIA_ROOT, md5 + '.exe').replace('\\', '/')
    imgfile = imgfile.replace('"', '')
    if os.path.exists(imgfile):
        data = open(imgfile, 'rb').read()

        # update_file_path文件存放位置
        file = open(imgfile, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/x-msdownload'
        # file_name下载下来保存的文件名字
        response['Content-Disposition'] = f"attachment; filename={escape_uri_path('CLodop_Setup_for_Win32NT.exe')};"
        return response
def excel_file_store( request):
    # 获取文件
    if request.method=='POST':
        files = request.FILES
        response = []
        # 取出文件的 key 和 value
        for key, value in files.items():
            # 读取文件
            content = value.read()
            md5 = hashlib.md5(content).hexdigest()
            # 指定文件路径
            path = os.path.join(MEDIA_ROOT, md5 + '.xls')

            with open(path, 'wb') as f:
                # 保存文件
                f.write(content)

        #读取文件内容,先简单判断文件是否合格;1.判断常规的几列是否存在
        path=path.replace('\\', '/')
        data=xlrd.open_workbook(path)   #打开文件
        sheet =data.sheet_by_index(0)  #默认每次就来发第一个sheet
        #rows=sheet.nrows  #总行数
        cols=sheet.ncols  #总列数
        cols_list=[]    #记录列内容
        sure_list = [] #记录需要列的下标识,记住标识是小一号的
        for i in range(cols): #列循环
            cols_list.append(sheet.cell(0,i).value.replace(' ',''))
            name=sheet.cell(0,i).value.replace(' ','')
            #if name != '站点' and name != '站点名称' and name != '商品' and name != '商品名称' and name != '销售数量' and name != '期末数量':
               # sheet.delete_cols(i) #删除此列

        if '类型' in cols_list and '级别' in cols_list and 'ERP单号' in cols_list and 'SKU编号' in cols_list and '产品名称' in cols_list  and '名字' in cols_list \
                and '单位' in cols_list and '分类' in cols_list and '数量' in cols_list and '合数' in cols_list  and '金额' in cols_list  and '颜色' in cols_list \
                and '字体' in cols_list and '物流' in cols_list and '包装方式' in cols_list and '尺寸' in cols_list and '客户备注' in cols_list and '生产日期' in cols_list\
                and '对单日期' in cols_list and '风格' in cols_list:
            #先删除多余的列,为计算增加速度站点编码	站点名称	城市代码	城市名称	等级
            return JsonResponse(data=md5, safe=False)
        else:
            return HttpResponse('nothing')
def auto_store(request):  #自动计算采购单数据
    post_data = request.body  # 获得页面数据
    post_data = json.loads(post_data)
    inform=post_data.get('inform')
    infile=inform.get('infile')  #上传文件的名字
    user_code = inform.get('create_user')  #获得用户的编号
    users = User.objects.filter(name=user_code).values('nameid')
    user_name = users[0].get('nameid')  #获得用户的名字
    ts = str(datetime.datetime.now().timestamp())  #生成时间戳,并转换为字符格式
    create_date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))  # 获取当前时间

    path = os.path.join(MEDIA_ROOT, infile + '.xls').replace('\\', '/') #得到路径
    path = path.replace('\\', '/')
    data = xlrd.open_workbook(path)  # 打开文件
    sheet = data.sheet_by_index(0)  # 默认每次就来发第一个sheet
    rows=sheet.nrows  #总行数
    cols = sheet.ncols  # 总列数
    cols_list = []  # 记录列内容
    sure_list = []  # 记录需要列的下标识,记住标识是小一号的forder_shen_sa
    for i in range(cols):  # 列循环
        cols_list.append(sheet.cell(0, i).value.replace(' ', ''))
    #将需要的几列下标计算出来
    if cols_list[0] =='类型' and cols_list[1] =='级别' and cols_list[2] =='ERP单号' and cols_list[3] =='SKU编号' and cols_list[4] =='产品名称' and cols_list[5] =='名字' and cols_list[6] =='单位' and cols_list[7] =='分类' \
        and cols_list[8] =='数量' and cols_list[9] =='合数' and cols_list[10] =='金额' and cols_list[11] =='颜色' and cols_list[12] =='字体' and cols_list[13] =='物流' \
        and cols_list[14] =='包装方式' and cols_list[15] =='尺寸' and cols_list[16] =='客户备注' and cols_list[17] =='生产日期' and cols_list[18] =='对单日期' and cols_list[19] =='风格':
        code =cop_order_excel()  #获取订单号
        j=0
        order_shen = []
        heji = 0  #合计初始化位0
        order_level = ''  #订单等级初始化
        for ii in range(1,rows): #行循环,第一行不算
            order_shen_i = Order_Del(order_key=code, order_type=sheet.cell(ii,0).value,order_level=sheet.cell(ii,1).value,
                                        order_code=str(sheet.cell(ii,2).value).replace('.0',''),item_code=sheet.cell(ii,3).value,
                                        item_name=sheet.cell(ii,4).value,order_name=sheet.cell(ii,5).value,
                                        unit=sheet.cell(ii,6).value,skutype=sheet.cell(ii,7).value,num=int(sheet.cell(ii,8).value),
                                        total_num=int(sheet.cell(ii,9).value),amount=sheet.cell(ii,10).value,
                                        color=sheet.cell(ii,11).value,words=sheet.cell(ii,12).value,
                                        wuliu=sheet.cell(ii,13).value,pack_method=sheet.cell(ii,14).value,
                                        size=sheet.cell(ii,15).value,note=sheet.cell(ii,16).value,
                                        create_date=sheet.cell(ii,17).value,end_date=sheet.cell(ii,18).value,sku_style=sheet.cell(ii,19).value)
            order_shen.append(order_shen_i)
            heji = heji + int(sheet.cell(ii,8).value)   #数量汇总
            order_level = sheet.cell(ii, 1).value
        Order_Del.objects.bulk_create(order_shen)
        order_tou=Order(id=code,date=inform.get('date'),salesman=user_name,note=inform.get('note'),create_user=user_code,add=inform.get('add'),total_num=heji,order_level=order_level,create_time=create_date)
        order_tou.save()
            # 返回前端信息
        return HttpResponse('OK')
    else:
        return HttpResponse(404)
def create_pi(request):
    post_data = request.body  # 获得页面数据
    post_data = json.loads(post_data)
    pi_list = post_data.get('data')  #获取完整的批次信息表
    print(pi_list)
    user_code = post_data.get('user')
    user_name = post_data.get('user_name')
    Date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))  # 获取当前时间
    #1.先获取最新的批次号码
    chache = pysql("exec PROC_ht_NumIndent ")
    pysql_update("insert into HT_num VALUES ('{}')".format(chache[0][0]))  # 单号插入记录表
    pi_order = 'HT'+chache[0][0]  #本批次单号
    #3.更新订单单身表信息
    num = 0
    for order_i in pi_list:
        Order_Del.objects.filter(order_key=order_i.get('id')).update(pi_code=pi_order,draw_status='正在画图')
        Order.objects.filter(id=order_i.get('id')).update(draw_status='正在画图',pi_code=pi_order)
        addr=Order.objects.filter(id=order_i.get('id')).values('add','order_level','note')
        add = addr[0].get('add')
        order_level=addr[0].get('order_level')
        note=addr[0].get('note')   #随机订单备注
        num = num+order_i.get('total_num')   #数量汇总
    # 2.将批次单头表插入批次基本信息
    pi_save = Draw_Pi(id=pi_order, create_time=Date, create_user=user_name,total_num=num,order_level=order_level,add=add,note=note)
    pi_save.save()
    #3.重新获取批次的明细列表
    data = {}
    pi_list = Order_Del.objects.filter(pi_code=pi_order).values() #获取全部内容
    pi_json = []
    for color_i in pi_list:
        pi_json.append(color_i)
    data['pi_list'] = pi_json
    data['pi_order'] = pi_order
    print(data)
    return JsonResponse(data=data,safe=False)
def draw_pi(request):    #获取画图批次信息
    #有权限区分,不同的人看到订单内容是不一样的
    post_data = request.body
    post_data = json.loads(post_data)
    user_id = post_data.get('user')  # 当前用户的账号信息
    # 获取用户的详细信息
    user_info = User.objects.filter(name=user_id).values()
    user_code = user_info[0].get('nameid')
    user_address = user_info[0].get('address')  # 获取地区
    user_radio = user_info[0].get('radio')  # 获取用户订单权限
    user_json = []
    user_data = {}
    if user_radio == '3':  # 标识全部订单
        if post_data.get('serch') == '' or post_data.get('serch') is None:
            user_list=Draw_Pi.objects.all().values().order_by('-id')
        else:
            pi_code = Order_Del.objects.filter(Q(order_key__icontains=post_data.get('serch'))|Q(order_code__icontains=post_data.get('serch'))).values('pi_code').distinct()
            if pi_code:
                pi_code=pi_code[0].get('pi_code')  #画图批次获取到了
                user_list = Draw_Pi.objects.filter(Q(id__icontains=post_data.get('serch'))|Q(create_time__icontains=post_data.get('serch'))|Q(create_time__icontains=post_data.get('serch'))
                                                   |Q(id__icontains=pi_code)).values().order_by('-id')
            else:
                user_list = Draw_Pi.objects.filter(
                    Q(id__icontains=post_data.get('serch')) | Q(create_time__icontains=post_data.get('serch')) | Q(create_time__icontains=post_data.get('serch'))).values().order_by('-id')
    elif user_radio == '2': #标识本地区所有的订单
        if post_data.get('serch') == '' or post_data.get('serch') is None:
            user_list=Draw_Pi.objects.filter(add=user_address).values().order_by('-id')
        else:
            user_list = Draw_Pi.objects.filter(add=user_address).values()
            pi_code = Order_Del.objects.filter(Q(order_key__icontains=post_data.get('serch'))|Q(order_code__icontains=post_data.get('serch'))).values('pi_code').distinct()
            if pi_code:
                pi_code=pi_code[0].get('pi_code')  #画图批次获取到了
                user_list = user_list.filter(Q(id__icontains=post_data.get('serch'))|Q(create_time__icontains=post_data.get('serch'))|Q(create_time__icontains=post_data.get('serch'))
                                                   |Q(id__icontains=pi_code)).values().order_by('-id')
            else:
                user_list = user_list.filter(
                    Q(id__icontains=post_data.get('serch')) | Q(create_time__icontains=post_data.get('serch')) | Q(create_time__icontains=post_data.get('serch'))).values().order_by('-id')
    elif user_radio == '1': #标识自由自己的订单
        if post_data.get('serch') == '' or post_data.get('serch') is None:
            user_list = Draw_Pi.objects.filter(create_user=user_code).values().order_by('-id')
        else:
            user_list = Draw_Pi.objects.filter(create_user=user_code).values()
            pi_code = Order_Del.objects.filter(Q(order_key__icontains=post_data.get('serch')) | Q(
                order_code__icontains=post_data.get('serch'))).values('pi_code').distinct()
            if pi_code:
                pi_code = pi_code[0].get('pi_code')  # 画图批次获取到了
                user_list = user_list.filter(
                    Q(id__icontains=post_data.get('serch')) | Q(create_time__icontains=post_data.get('serch')) | Q(
                        create_time__icontains=post_data.get('serch'))
                    | Q(id__icontains=pi_code)).values().order_by('-id')
            else:
                user_list = user_list.filter(
                    Q(id__icontains=post_data.get('serch')) | Q(create_time__icontains=post_data.get('serch')) | Q(
                        create_time__icontains=post_data.get('serch'))).values().order_by('-id')

    user_page=Paginator(user_list,post_data.get('size')).page(post_data.get('page'))
    total= Paginator(user_list,post_data.get('size')).count    #总计的数量
    user_data['user_list']=list(user_page)
    user_data['total']=total
    return JsonResponse(data=user_data,safe=False)
def draw_page_get(request):
    post_data = request.body  # 获得页面数据
    post_data = json.loads(post_data)
    order_num = post_data.get('order')  # 得到批次号
    order_tou = Draw_Pi.objects.filter(id=order_num).values()
    order_tou = order_tou[0]
    order_shen_json = []
    order_shen_jin = Order_Del.objects.filter(pi_code=order_num,color='金色')  #获得本批次所有的订单
    order_shen_jin = order_shen_jin.exclude(state='关闭').values().order_by('order_name')
    for order_i_jin in order_shen_jin:
        order_shen_json.append(order_i_jin)

    order_shen_bai = Order_Del.objects.filter(pi_code=order_num, color='白金')  # 获得本批次所有的订单
    order_shen_bai = order_shen_bai.exclude(state='关闭').values().order_by('order_name')
    for order_i_bai in order_shen_bai:
        order_shen_json.append(order_i_bai)

    order_shen_mei = Order_Del.objects.filter(pi_code=order_num, color='玫瑰金')  # 获得本批次所有的订单
    order_shen_mei = order_shen_mei.exclude(state='关闭').values().order_by('order_name')
    for order_i_mei in order_shen_mei:
        order_shen_json.append(order_i_mei)

    order_shen_qita = Order_Del.objects.filter(pi_code=order_num)  # 获得本批次所有的订单
    order_shen_qita = order_shen_qita.exclude(color='金色')
    order_shen_qita = order_shen_qita.exclude(state='关闭')
    order_shen_qita = order_shen_qita.exclude(color='玫瑰金')
    order_shen_qita = order_shen_qita.exclude(color='白金').values().order_by('order_name')
    for order_i_qita in order_shen_qita:
        order_shen_json.append(order_i_qita)

    data = {}
    data['tou'] = order_tou
    data['shen'] = order_shen_json
    return JsonResponse(data=data, safe=False)
def print_draw(request):  #打印画图批次
    post_data = request.body  # 获得页面数据
    post_data = json.loads(post_data)
    order_num = post_data.get('order')  # 得到批次号
    order_shen_json = []
    order_shen = Order_Del.objects.filter(pi_code=order_num).values()   #获得本批次所有的订单
    color_json = []
    for color_i in order_shen:
        color_json.append(color_i)
    return JsonResponse(data=color_json, safe=False)
def delete_draw_pi (request): #删除订单批次
    post_data = request.body  # 获得页面数据
    post_data = json.loads(post_data)
    name = post_data.get('name')
    Draw_Pi.objects.filter(id=name).delete()
    Order_Del.objects.filter(pi_code=name).update(pi_code ='',draw_status='未画图')
    Order.objects.filter(pi_code=name).update(pi_code ='',draw_status='未画图')
    return HttpResponse('OK')
def draw_Approval(request):
    date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))  # 获取当前时间
    post_data = request.body  # 获得页面数据
    post_data = json.loads(post_data)
    order_num = post_data.get('order')  #获得批次单号
    user = post_data.get('user')    #获得用户人账号
    user_name = User.objects.filter(name=user).values('nameid')  #获得用户人姓名
    user_name = user_name[0].get('nameid')  #获得当前上传员工的名字

    Order_Del.objects.filter(pi_code=order_num).update(draw_status='画图完成',draw_time=date,draw_user=user_name)
    Order.objects.filter(pi_code=order_num).update(draw_status='画图完成')
    Draw_Pi.objects.filter(id=order_num).update(status='画图完成',complete_time=date,draw_user=user_name)
    return HttpResponse('OK')
def draw_Approval_cancel(request):
    date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))  # 获取当前时间
    post_data = request.body  # 获得页面数据
    post_data = json.loads(post_data)
    order_num = post_data.get('order')  #获得批次单号
    user = post_data.get('user')    #获得用户人账号
    user_name = User.objects.filter(name=user).values('nameid')  #获得用户人姓名
    user_name = user_name[0].get('nameid')  #获得当前上传员工的名字

    Order_Del.objects.filter(pi_code=order_num).update(draw_status='未画图',draw_time='',draw_user='')
    Order.objects.filter(pi_code=order_num).update(draw_status='未画图')
    Draw_Pi.objects.filter(id=order_num).update(status='未画图',complete_time='',draw_user='')
    return HttpResponse('OK')
def order_complete(request):   #查找状态是画图完成或者是拉图完成的明细
    post_data = request.body
    post_data = json.loads(post_data)
    user_json = []
    user_data = {}
    selectForm = post_data.get('serch')
    if selectForm.get('draw_time') or selectForm.get('print_time') or selectForm.get('order_code') or selectForm.get('draw_status') or selectForm.get(
            'order_level') or selectForm.get('color') or selectForm.get('words') or selectForm.get('print_status')  or selectForm.get('item_name')\
            or selectForm.get('type') or selectForm.get('order_name') or selectForm.get('salesman'):
        user_list = Order_Del.objects.filter(Q(draw_status='画图完成')|Q(draw_status='拉图完成')|Q(draw_status='待拉图'))
        if selectForm.get('draw_time'): #画图时间
            draw_time = selectForm.get('draw_time')
            begin_draw = draw_time[0][:10] + ' 00:00'
            end_draw = draw_time[1][:10] + ' 24:00'
            print(draw_time,begin_draw,end_draw)
            user_list = user_list.filter(draw_time__gte=begin_draw, draw_time__lte=end_draw)
        if selectForm.get('print_time'): #画图时间
            draw_time = selectForm.get('print_time')
            begin_draw = draw_time[0][:10] + ' 00:00'
            end_draw = draw_time[1][:10] + ' 24:00'
            user_list = user_list.filter(print_time__gte=begin_draw, print_time__lte=end_draw)
        if selectForm.get('order_code'):
            user_list = user_list.filter(order_code__contains=selectForm.get('order_code'))
        if selectForm.get('draw_status'):
            user_list = user_list.filter(draw_status=selectForm.get('draw_status'))
        if selectForm.get('order_level'):
            user_list = user_list.filter(order_level=selectForm.get('order_level'))
        if selectForm.get('color'):
            user_list = user_list.filter(color=selectForm.get('color'))
        if selectForm.get('words'):
            user_list = user_list.filter(words=selectForm.get('words'))
        if selectForm.get('type'):
            user_list = user_list.filter(skutype=selectForm.get('type'))
        if selectForm.get('order_name'):
            user_list = user_list.filter(order_name__contains=selectForm.get('order_name'))
        if selectForm.get('salesman'):
            user_list = user_list.filter(salesman__contains=selectForm.get('salesman_code'))
        if selectForm.get('print_status'):
            user_list = user_list.filter(print_status__contains=selectForm.get('print_status'))
        if selectForm.get('item_name'):
            user_list = user_list.filter(item_name__contains=selectForm.get('item_name'))
        user_list = user_list.values().order_by('-id')  # 转换取值

    else:
        user_list = Order_Del.objects.filter(Q(draw_status='画图完成')|Q(draw_status='拉图完成')|Q(draw_status='待拉图')).values().order_by('-id')
    user_page = Paginator(user_list, post_data.get('size')).page(post_data.get('page'))
    total = Paginator(user_list, post_data.get('size')).count  # 总计的数量
    user_data['user_list'] = list(user_page)
    user_data['total'] = total
    return JsonResponse(data=user_data, safe=False)
def draw_agin(request):
    post_data = request.body  # 获得页面数据
    post_data = json.loads(post_data)
    pi_list = post_data.get('data')
    #.更新订单单身表信息,将画图完成,更新为拉图完成
    for order_i in pi_list:
        Order_Del.objects.filter(id=order_i.get('id')).update(draw_status='待拉图')
    return HttpResponse('OK')
def draw_again_del(request):
    post_data = request.body
    post_data = json.loads(post_data)
    user_json = []
    user_data = {}
    selectForm = post_data.get('serch')
    user = post_data.get('user')
    print(selectForm)
    if selectForm.get('date') or selectForm.get('order_code') or selectForm.get('draw_status') or selectForm.get('order_level') or selectForm.get('color') or selectForm.get('words')\
            or selectForm.get('type') or selectForm.get('order_name') or selectForm.get('salesman'):
        user_list=Order_Del.objects.filter(draw_user=user,draw_status='待拉图')
        if selectForm.get('date'):
            print(selectForm.get('date'))
        if selectForm.get('order_code'):
            user_list=user_list.filter(order_code__contains=selectForm.get('order_code'))
        if selectForm.get('draw_status'):
            user_list=user_list.filter(draw_status=selectForm.get('draw_status'))
        if selectForm.get('order_level'):
            user_list=user_list.filter(order_level=selectForm.get('order_level'))
        if selectForm.get('color'):
            user_list=user_list.filter(color=selectForm.get('color'))
        if selectForm.get('words'):
            user_list=user_list.filter(words=selectForm.get('words'))
        if selectForm.get('type'):
            user_list = user_list.filter(skutype=selectForm.get('type'))
        if selectForm.get('order_name'):
            user_list = user_list.filter(order_name__contains=selectForm.get('order_name'))
        if selectForm.get('salesman'):
            user_list = user_list.filter(salesman__contains=selectForm.get('salesman_code'))
        user_list=user_list.values().order_by('-id')   #转换取值

    else:
        user_list = Order_Del.objects.filter(draw_user=user,draw_status='待拉图').values().order_by('-id')
    user_page = Paginator(user_list, post_data.get('size')).page(post_data.get('page'))
    total = Paginator(user_list, post_data.get('size')).count  # 总计的数量
    for user_i in user_page:
        user_json.append(user_i)
    user_data['user_list'] = user_json
    user_data['total'] = total
    return JsonResponse(data=user_data, safe=False)
def order_del_close(request):  #关闭订单明细行
    post_data=request.body  #获得页面数据
    post_data=json.loads(post_data)
    id=post_data.get('id')
    Order_Del.objects.filter(id=id).update(state='关闭')
    return HttpResponse('OK')
def print_status(request):
    Date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))  # 获取当前时间
    post_data = request.body  # 获得页面数据
    post_data = json.loads(post_data)
    id = post_data.get('id') #获取后台的id
    user = post_data.get('user') #获取后台的id
    Order_Del.objects.filter(id=id).update(print_status = '已打印',print_time = Date,print_user=user)
    return  HttpResponse('OK')
def update_print_status(request):
    post_data = request.body  # 获得页面数据
    post_data = json.loads(post_data)
    pi_list = post_data.get('data')
    #.更新订单单身表信息,将画图完成,更新为拉图完成
    for order_i in pi_list:
        Order_Del.objects.filter(id=order_i.get('id')).update(print_status='未打印',print_time='',print_user = '')
    return HttpResponse('OK')
def draw_list_all(request):
    post_data = request.body
    user_json = []
    post_data = json.loads(post_data)
    user_data = {}
    selectForm = post_data.get('serch')
    date = selectForm.get('date')
    if date:
        begin_date=date[0][:10]+' 00:00'
        end_date=date[1][:10]+' 24:00'
    user_code= selectForm.get('user_code') #账号信息

    if date:  #标识日期存在
        user_list=Order_Del.objects.filter(draw_time__gte=begin_date,draw_time__lte=end_date)
        if user_code == '': #为空标识所有人
            user_list = user_list.filter(Q(draw_status='画图完成') | Q(draw_status='拉图完成')).values().order_by('-id')
        else: #人员不为空
            user_list = user_list.filter((Q(draw_status='画图完成') | Q(draw_status='拉图完成')),Q(draw_user=user_code)).values().order_by('-id')
    else: #日期不存在
        if user_code == '': #为空标识所有人
            user_list = Order_Del.objects.filter(Q(draw_status='画图完成') | Q(draw_status='拉图完成')).values().order_by('-id')
        else: #人员不为空
            user_list = Order_Del.objects.filter((Q(draw_status='画图完成') | Q(draw_status='拉图完成')),Q(draw_user=user_code)).values().order_by('-id')
    user_page = Paginator(user_list, post_data.get('size')).page(post_data.get('page'))
    total = Paginator(user_list, post_data.get('size')).count  # 总计的数量
    for user_i in user_page:
        user_json.append(user_i)
    user_data['user_list'] = user_json
    user_data['total'] = total
    return JsonResponse(data=user_data, safe=False)
def order_track(request):   #查找状态是画图完成或者是拉图完成的明细
    post_data = request.body
    post_data = json.loads(post_data)
    user_json = []
    user_data = {}
    selectForm = post_data.get('serch')
    print(selectForm)
    if selectForm.get('draw_time') or selectForm.get('print_time') or selectForm.get('order_code') or selectForm.get('draw_status') or selectForm.get(
            'order_level') or selectForm.get('color') or selectForm.get('words') or selectForm.get('print_status')  or selectForm.get('item_name')\
            or selectForm.get('type') or selectForm.get('order_name') or selectForm.get('salesman'):
        user_list = Order_Del.objects.all()
        if selectForm.get('draw_time'): #画图时间
            draw_time = selectForm.get('draw_time')
            begin_draw = draw_time[0][:10] + ' 00:00'
            end_draw = draw_time[1][:10] + ' 24:00'
            user_list = user_list.filter(draw_time__gte=begin_draw, draw_time__lte=end_draw)
        if selectForm.get('print_time'): #画图时间
            draw_time = selectForm.get('print_time')
            begin_draw = draw_time[0][:10] + ' 00:00'
            end_draw = draw_time[1][:10] + ' 24:00'
            user_list = user_list.filter(print_time__gte=begin_draw, print_time__lte=end_draw)
        if selectForm.get('order_code'):
            user_list = user_list.filter(order_code__contains=selectForm.get('order_code'))
        if selectForm.get('draw_status'):
            user_list = user_list.filter(draw_status=selectForm.get('draw_status'))
        if selectForm.get('order_level'):
            user_list = user_list.filter(order_level=selectForm.get('order_level'))
        if selectForm.get('color'):
            user_list = user_list.filter(color=selectForm.get('color'))
        if selectForm.get('words'):
            user_list = user_list.filter(words=selectForm.get('words'))
        if selectForm.get('type'):
            user_list = user_list.filter(skutype=selectForm.get('type'))
        if selectForm.get('order_name'):
            user_list = user_list.filter(order_name__contains=selectForm.get('order_name'))
        if selectForm.get('salesman'):
            user_list = user_list.filter(salesman__contains=selectForm.get('salesman'))
        if selectForm.get('print_status'):
            user_list = user_list.filter(print_status__contains=selectForm.get('print_status'))
        if selectForm.get('item_name'):
            user_list = user_list.filter(item_name__contains=selectForm.get('item_name'))
        user_list = user_list.values().order_by('-id')  # 转换取值

    else:
        user_list = Order_Del.objects.all().values().order_by('-id')
    user_page = Paginator(user_list, post_data.get('size')).page(post_data.get('page'))
    total = Paginator(user_list, post_data.get('size')).count  # 总计的数量
    user_data['user_list'] = list(user_page)
    user_data['total'] = total
    return JsonResponse(data=user_data, safe=False)
def warehouse(request):    #获取库存明细
    #有权限区分,不同的人看到订单内容是不一样的
    post_data = request.body
    post_data = json.loads(post_data)
    user_json = []
    user_data={}
    if post_data.get('serch') == '' or post_data.get('serch') is None:
        user_list=Warehousing.objects.filter(type='入库').values().order_by('-id')
    else:
        user_list = Warehousing.objects.filter(Q(type='入库'),Q(id__icontains=post_data.get('serch'))|Q(date__icontains=post_data.get('serch'))|Q(note__icontains=post_data.get('serch'))).values().order_by('-id')
    user_page=Paginator(user_list,post_data.get('size')).page(post_data.get('page'))
    total= Paginator(user_list,post_data.get('size')).count    #总计的数量
    for user_i in user_page:
        user_json.append(user_i)
    user_data['user_list']=user_json
    user_data['total']=total
    return JsonResponse(data=user_data,safe=False)
def warehouse_out(request):    #获取库存明细
    #有权限区分,不同的人看到订单内容是不一样的
    post_data = request.body
    post_data = json.loads(post_data)
    user_json = []
    user_data={}
    if post_data.get('serch') == '' or post_data.get('serch') is None:
        user_list=Warehousing.objects.filter(type='出库').values().order_by('-id')
    else:
        user_list = Warehousing.objects.filter(Q(type='出库'),Q(id__icontains=post_data.get('serch'))|Q(date__icontains=post_data.get('serch'))|Q(note__icontains=post_data.get('serch'))).values().order_by('-id')
    user_page=Paginator(user_list,post_data.get('size')).page(post_data.get('page'))
    total= Paginator(user_list,post_data.get('size')).count    #总计的数量
    for user_i in user_page:
        user_json.append(user_i)
    user_data['user_list']=user_json
    user_data['total']=total
    return JsonResponse(data=user_data,safe=False)
def Stock_del(request):    #获取
    post_data = request.body
    post_data = json.loads(post_data)
    user_json = []
    user_data={}
    if post_data.get('serch') == '' or post_data.get('serch') is None:
        user_list=Stock.objects.all().values()
    else:
        user_list = Stock.objects.filter(Q(item_code__icontains=post_data.get('serch'))|Q(item_name__icontains=post_data.get('serch'))).values()
    user_page=Paginator(user_list,post_data.get('size')).page(post_data.get('page'))
    total= Paginator(user_list,post_data.get('size')).count    #总计的数量
    for user_i in user_page:
        user_json.append(user_i)
    user_data['user_list']=user_json
    user_data['total']=total
    return JsonResponse(data=user_data,safe=False)
def contacts(request):
    post_data = request.body
    post_data = json.loads(post_data)
    user_json = []
    user_data = {}
    if post_data.get('serch') == '' or post_data.get('serch') is None:
        user_list = Contacts.objects.all().values()
    else:
        user_list = Contacts.objects.filter(
            Q(id__icontains=post_data.get('serch')) | Q(name__icontains=post_data.get('serch'))).values()
    user_page = Paginator(user_list, post_data.get('size')).page(post_data.get('page'))
    total = Paginator(user_list, post_data.get('size')).count  # 总计的数量
    for user_i in user_page:
        user_json.append(user_i)
    user_data['sku_list'] = user_json
    user_data['total'] = total
    return JsonResponse(data=user_data, safe=False)
def cl_sku(request):
    post_data = request.body
    post_data = json.loads(post_data)
    user_json = []
    user_data = {}
    if post_data.get('serch') == '' or post_data.get('serch') is None:
        user_list = cl_SKU.objects.all().values()
    else:
        user_list = cl_SKU.objects.filter(Q(id__icontains=post_data.get('serch')) | Q(name__icontains=post_data.get('serch'))).values()
    user_page = Paginator(user_list, post_data.get('size')).page(post_data.get('page'))
    total = Paginator(user_list, post_data.get('size')).count  # 总计的数量
    for user_i in user_page:
        user_json.append(user_i)
    user_data['sku_list'] = user_json
    user_data['total'] = total
    return JsonResponse(data=user_data, safe=False)
def get_user_add(request):
    post_data=request.body  #获得页面数据
    post_data=json.loads(post_data)
    user_code = post_data.get('user_code') #获取用户编码
    user_add = User.objects.filter(name=user_code).values('address')
    return HttpResponse(user_add[0].get('address'))
def excel_out(request): #导出表格
    date_miao = time.strftime('%Y%m%d%H%M%S', time.localtime())  #时间戳
    post_data = request.body
    post_data = json.loads(post_data)
    pi_num = post_data.get('pi_num')
    ahttp= 'http://47.114.190.252:8888/img?md5='   #产品图片地址
    ahttp_order= 'http://47.114.190.252:8888/img_order?md5='  #订单图片地址
        #处理表格
    new_excel = xlwt.Workbook(encoding='udf-8')
    new_sheet = new_excel.add_sheet('导出画图批次')  # 创建excel

    new_sheet.write(0, 0, '类型')  # 列头
    new_sheet.write(0, 1, '级别')  # 列头
    new_sheet.write(0, 2, 'ERP单号')
    new_sheet.write(0, 3, '名字')
    new_sheet.write(0, 4, 'SKU编号')
    new_sheet.write(0, 5, '产品名称')
    new_sheet.write(0, 6, '分类')
    new_sheet.write(0, 7, '数量')
    new_sheet.write(0, 8, '合数')
    new_sheet.write(0, 9, '物流')
    new_sheet.write(0, 10, '包装方式')  # 站点编码
    new_sheet.write(0, 11, '链长')  # 排序字段
    new_sheet.write(0, 12, '颜色')
    new_sheet.write(0, 13, '字体')
    new_sheet.write(0, 14, '风格')
    new_sheet.write(0, 15, '备注')
    new_sheet.write(0, 16, '金额')
    new_sheet.write(0, 17, '交货日期')
    new_sheet.write(0, 18, '产品图片')
    new_sheet.write(0, 19, '订单图片')
    #读取数据库的内容化
    order_del = Order_Del.objects.filter(pi_code=pi_num).values()
    i = 1 #定义行数
    if order_del:
        for jt_i in order_del:
            new_sheet.write(i, 0,jt_i.get('order_type'))  # 列头
            new_sheet.write(i, 1, 'order_level')  # 列头
            new_sheet.write(i, 2, jt_i.get('order_code'))
            new_sheet.write(i, 3, jt_i.get('item_code'))
            new_sheet.write(i, 4, jt_i.get('item_name'))
            new_sheet.write(i, 5, jt_i.get('sku_name'))
            new_sheet.write(i, 6, jt_i.get('skutype'))
            new_sheet.write(i, 7, jt_i.get('num'))
            new_sheet.write(i, 8, jt_i.get('total_num'))
            new_sheet.write(i, 9, jt_i.get('wuliu'))
            new_sheet.write(i, 10, jt_i.get('pack_method'))  # 站点编码
            new_sheet.write(i, 11, jt_i.get('size'))  # 排序字段
            new_sheet.write(i, 12, jt_i.get('color'))
            new_sheet.write(i, 13, jt_i.get('words'))
            new_sheet.write(i, 14, jt_i.get('sku_style'))
            new_sheet.write(i, 15, jt_i.get('note'))
            new_sheet.write(i, 16, jt_i.get('amount'))
            new_sheet.write(i, 17, jt_i.get('end_date'))

            imgfile = os.path.join(MEDIA_ROOT, jt_i.get('picture') + '.jpg').replace('\\', '/')
            imgfile = imgfile.replace('"', '')
            if os.path.exists(imgfile):
                new_sheet.insert_image(i,18,imgfile)
            else:  # 检索不到jpg格式时
                imgfile = os.path.join(MEDIA_ROOT, jt_i.get('picture') + '.jpeg').replace('\\', '/')
                imgfile = imgfile.replace('"', '')
                if os.path.exists(imgfile):
                    new_sheet.insert_image(i,18,imgfile)
                else:  # 标识jpeg格式也没有找到
                    imgfile = os.path.join(MEDIA_ROOT, jt_i.get('picture') + '.png').replace('\\', '/')
                    imgfile = imgfile.replace('"', '')
                    if os.path.exists(imgfile):
                        new_sheet.insert_image(i,18,imgfile)

            imgfile_order = os.path.join(MEDIA_ROOT,'order/', jt_i.get('order_img') + '.jpg').replace('\\', '/')
            imgfile = imgfile.replace('"', '')
            if os.path.exists(imgfile):
                new_sheet.insert_image(i, 19, imgfile)
            else:  # 检索不到jpg格式时
                imgfile = os.path.join(MEDIA_ROOT, 'order/',jt_i.get('order_img') + '.jpeg').replace('\\', '/')
                imgfile = imgfile.replace('"', '')
                if os.path.exists(imgfile):
                    new_sheet.insert_image(i, 19, imgfile)
                else:  # 标识jpeg格式也没有找到
                    imgfile = os.path.join(MEDIA_ROOT,'order/', jt_i.get('order_img') + '.png').replace('\\', '/')
                    imgfile = imgfile.replace('"', '')
                    if os.path.exists(imgfile):
                        new_sheet.insert_image(i, 19, imgfile)
            #行数加一
            i=i+1
        #保存表格到服务器
        path = os.path.join(MEDIA_ROOT,'excel_out/', date_miao + '.xls')
        new_excel.save(r'{}'.format(path))  # 保存表格\
        return HttpResponse(date_miao)
    else:
        return HttpResponse('Nothing')
def draw_print(request):
    post_data=request.body
    post_data=json.loads(post_data)
    id = post_data.get('id')
    aa=Draw_Pi.objects.filter(id=id).update(print_status='已打印')
    return HttpResponse('OK')
def update_draw(request):
    post_data=request.body
    post_data=json.loads(post_data)
    data = post_data.get('data')
    id = data.get('id')
    draw_user = data.get('draw_user')
    complete_time = data.get('complete_time')

    aa=Draw_Pi.objects.filter(id=id).update(draw_user=draw_user,complete_time=complete_time)
    return HttpResponse('OK')
