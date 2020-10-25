from django.db import models

# Create your models here.
class User(models.Model):  #用户信息表
    name=models.CharField(max_length=20,primary_key=True) #账号
    nameid=models.CharField(max_length=20,null=True) #姓名
    password=models.CharField(max_length=20,null=False)
    email=models.CharField(max_length=20,null=True)
    iphone=models.CharField(max_length=20,null=True)
    jiaose=models.CharField(max_length=20,null=True)
    status=models.BooleanField( default=True)
    address=models.CharField(max_length=20,null=True)
    role=models.CharField(max_length=20,null=True)#用户的角色
    radio=models.CharField(max_length=4,null=True,default='1')#订单数据权限
class quanxian(models.Model):
    code_name=models.CharField(max_length=20,null=False)
    jon_code=models.CharField(max_length=20,null=False)
    job_name=models.CharField(max_length=20,null=False)
    level=models.CharField(max_length=2,null=True)  #层级
    sort=models.CharField(max_length=4,null=True)  #排序
class Color(models.Model):  #颜色信息
    color_id=models.CharField(max_length=20,primary_key=True) #账号
    color_name=models.CharField(max_length=30,null=True) #姓名
class Size(models.Model):  #尺寸信息
    size_id=models.CharField(max_length=20,primary_key=True) #账号
    size_name=models.CharField(max_length=30,null=True) #名字
class Style(models.Model):  #产品分类
    id=models.CharField(max_length=20,primary_key=True) #编号
    name=models.CharField(max_length=30,null=True) #名字
class Pack_method(models.Model):  #产品分类
    id=models.CharField(max_length=20,primary_key=True) #编号
    name=models.CharField(max_length=30,null=True) #名字
class SkuType(models.Model):  #产品分类
    id=models.CharField(max_length=20,primary_key=True) #编号
    name=models.CharField(max_length=30,null=True) #姓名
class SKU(models.Model):  #产品分类
    id=models.CharField(max_length=20,primary_key=True) #编号
    name=models.CharField(max_length=40,null=False) #
    type=models.CharField(max_length=40,null=True) #
    unit=models.CharField(max_length=20,null=True) #修改为了风格
    barcode=models.CharField(max_length=255,null=True) #  原条码字段修改为了说明
    picture=models.CharField(max_length=20,null=True)
    people=models.CharField(max_length=20,null=True)
    create_date=models.CharField(max_length=20,null=True)
    status=models.BooleanField( default=True)   #状态
    imageUrl=models.CharField( max_length=100,null=True)   #图片
    price = models.FloatField(default=0)  # 包装单价
    draw_price = models.FloatField(default=0)  # 画图单价
    style_num = models.FloatField(default=0)  # 画图单价
    cost_price = models.FloatField(default=0)  # 成本单价
class Wuliu(models.Model):  #颜色信息
    id=models.CharField(max_length=20,primary_key=True) #账号
    name=models.CharField(max_length=30,null=True) #姓名
class Wenzi(models.Model):  #颜色信息
    id=models.CharField(max_length=20,primary_key=True) #账号
    name=models.CharField(max_length=30,null=True) #姓名
class Order(models.Model):
    id = models.CharField(max_length=20, primary_key=True)  # 单号
    date=models.CharField(max_length=40,null=True) #
    add=models.CharField(max_length=40,null=True) #
    note=models.CharField(max_length=200,null=True) #
    salesman = models.CharField(max_length=40, null=True)  #
    create_time = models.CharField(max_length=40, null=True)  #
    examine = models.CharField(max_length=40, null=True)  # 审核人
    examine_time = models.CharField(max_length=40, null=True)  # 审核时间
    create_user = models.CharField(max_length=40, null=True)  #创建人
    update_time = models.CharField(max_length=40, null=True)  # 修改时间
    update_user = models.CharField(max_length=40, null=True)  # 修改人
    total_num = models.IntegerField(default=0) #单头数量合计
    total_amount  = models.FloatField(max_length=20,default=0) #金额汇总
    order_level = models.CharField(max_length=10, null=True)  # 订单级别
    draw_status = models.CharField(max_length=10, null=True, default='未画图')  # 单头画图状态,未画图--正在画图 ---画图完成
    status = models.CharField(max_length=10, null=True, default='未审核')  # 审核状态,审核,未审核
    pi_code = models.CharField(max_length=30, null=True)  # 画图批次号
class Order_Del(models.Model):                       #订单单身信息
    order_key = models.CharField(max_length=20,default='')  # 单号,系统生成的单号
    order_code = models.CharField(max_length=20)  # 单号,平台上的单号
    item_code = models.CharField(max_length=20)
    item_name = models.CharField(max_length=200)
    order_name = models.CharField(max_length=200,null=True) #订单自定义的名字
    unit = models.CharField(max_length=10)
    skutype = models.CharField(max_length=20)
    color = models.CharField(max_length=20)
    words = models.CharField(max_length=30)
    num = models.IntegerField(max_length=10)
    total_num = models.IntegerField(max_length=10,null=True,default=0)
    wuliu = models.CharField(max_length=30)
    lianchang = models.IntegerField(max_length=20,null=True,default=0)
    note = models.CharField(max_length=200,null=True)
    size = models.CharField(max_length=20,null=True,default='')
    create_date = models.CharField(max_length=30,null=True)
    end_date = models.CharField(max_length=30,null=True)
    state = models.CharField(max_length=20,default='未审核')   #状态  未审核--审核---关闭  //同时记录关闭状态
    order_type = models.CharField(max_length=10,null=True)   #订单类型
    pack_method = models.CharField(max_length=20,null=True)   #包装方式
    order_level = models.CharField(max_length=10,null=True)   #订单级别
    sku_style = models.CharField(max_length=30,null=True)   #SKU风格
    draw_status = models.CharField(max_length=10,null=True,default='未画图')   #画图状态,未画图--正在画图 ---画图完成--待拉图--拉图完成
    draw_time = models.CharField(max_length=20, null=True, default='')  #画图完成时间
    draw_again_time = models.CharField(max_length=20, null=True, default='')  #拉图完成时间
    draw_user = models.CharField(max_length=20, null=True, default='')  #画图人员账号
    draw_name = models.CharField(max_length=20, null=True, default='')  #画图人员名称
    print_status = models.CharField(max_length=30, default='未打印')  # 打印状态
    print_time = models.CharField(max_length=30, default='null')  # 打印时间
    page_status = models.CharField(max_length=10,null=True,default='未包装')   #包装状态
    print_user = models.CharField(max_length=20,null=True,default='')   #打印人账号
    chuku_status = models.CharField(max_length=10,null=True,default='未出库')   #出库状态--已出库--未出库
    order_img = models.CharField(max_length=200,null=True)   #订单图片
    picture = models.CharField(max_length=200,null=True)   #产品图片
    draw_img = models.CharField(max_length=200,null=True)   #画图图片地址
    amount  = models.FloatField(max_length=20, null=True, default=0) #金额
    salesman = models.CharField(max_length=40, null=True)  #业务员,传递单头的信息
    date = models.CharField(max_length=40, null=True)  #订单日期
    packing_num = models.IntegerField(default=0)     #打包数量
    pi_code = models.CharField(max_length=30,default='')   #画图生成的批次号码
    update_status = models.IntegerField(max_length=10,default=0)  #无用字段,仅仅为了前端用的
    draw_price = models.FloatField(default=0)  # 画图单价
    style_num = models.FloatField(default=0)  # 画图款式
    draw_amount = models.FloatField(default=0)  # 画图金额
class packing(models.Model):
    order_key = models.IntegerField( default=0)  # 订单号单身主键key
    user_code = models.CharField(max_length=20,null=True)
    date = models.CharField(max_length=20,null=True)
    order_code = models.CharField(max_length=20,null=True) #订单编号
    name = models.CharField(max_length=20,null=True) #订单上的名字
    item_code = models.CharField(max_length=20,null=True) #产品编码
    item_name = models.CharField(max_length=100,null=True) #产品名称
    total_num = models.IntegerField(default=0) #订单的合数
    packing_num = models.IntegerField(default=0) #本次的加工量
    wuliu = models.CharField(max_length=30)
    color = models.CharField(max_length=20)
    words = models.CharField(max_length=30)
    lianchang = models.IntegerField(max_length=20, null=True, default=0)
    price = models.FloatField(default=0)    #单价
class Roles(models.Model):  #角色名称表
    role_name = models.CharField(max_length=40,null=False) #角色名称
    role_explain = models.CharField(max_length=100,null=True)  #角色描述
class Roles_Del(models.Model): #角色详情表
    role_name = models.CharField(max_length=40, null=False)  # 角色名称,以下内容和权限一样了
    code_name = models.CharField(max_length=20, null=False,default='null')
    jon_code = models.CharField(max_length=20, null=False,default='null')
    job_name = models.CharField(max_length=20, null=False,default='null')
    level = models.CharField(max_length=2, null=True)
    sort = models.CharField(max_length=4, null=True)  # 排序
class Draw_Pi(models.Model): #画图批次记录信息表
    id  = models.CharField(max_length=20, primary_key=True)  # 标识批次号
    status= models.CharField(max_length=10,null=True,default='未画图')
    print_status= models.CharField(max_length=10,null=True,default='未打印')  #打印状态
    create_time = models.CharField(max_length=40, null=True)  #创建时间
    create_user = models.CharField(max_length=40, null=True)  # 创建人
    add = models.CharField(max_length=40, null=True)  #地址
    total_num = models.IntegerField(default=0)  # 数量合计
    order_level = models.CharField(max_length=10, null=True)  # 订单级别
    draw_user = models.CharField(max_length=40, null=True)  # 画图人
    complete_time = models.CharField(max_length=40, null=True)  # 画图完成时间
    note = models.CharField(max_length=200, null=True)  #备注信息
class Warehousing(models.Model): #入库信息表
    id = models.CharField(max_length=20, primary_key=True)  # 单号
    date = models.CharField(max_length=40, null=True)  #
    note = models.CharField(max_length=200, null=True)  #
    supplier_ware = models.CharField(max_length=200, null=True)  #供应商
    create_time = models.CharField(max_length=40, null=True)  #
    examine = models.CharField(max_length=40, null=True)  # 审核人
    examine_time = models.CharField(max_length=40, null=True)  # 审核时间
    create_user = models.CharField(max_length=40, null=True)  # 创建人
    type = models.CharField(max_length=40, null=True,default='入库')  # 类型--出库--入库
class Warehous_Del(models.Model):                       #订单单身信息,准备将出入库全部放入一个表中
    order_key = models.CharField(max_length=20,default='')  # 单号,系统生成的单号
    item_code = models.CharField(max_length=20)
    item_name = models.CharField(max_length=200)
    format = models.CharField(max_length=20)
    unit = models.CharField(max_length=20,default='')  #单位
    num = models.IntegerField()  #入库数量
    price = models.FloatField(default=0)   #单价
    total = models.IntegerField(default=0)  #金额合计
    note = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=20,default='未审核')   #状态  未审核--审核---关闭  //同时记录关闭状态
    create_user = models.CharField(max_length=40, null=True)  # 创建人
    date = models.CharField(max_length=40, null=True)  #单据日期
    supplier_ware = models.CharField(max_length=200, null=True)  # 供应商
class Contacts(models.Model): #往来对象信息
    id = models.CharField(max_length=30, primary_key=True)  # 编码
    name = models.CharField(max_length=100, null=True)  #名称
    people = models.CharField(max_length=20, null=True)  #
    phone = models.CharField(max_length=20, null=True)  #
    address = models.CharField(max_length=220, null=True)  #
    note = models.CharField(max_length=220, null=True)  #
    create_date = models.CharField(max_length=20, null=True)  #
    create_user = models.CharField(max_length=20, null=True)  #
    status = models.BooleanField(default=True)  # 状态是否停用
class cl_SKU(models.Model):
    id = models.CharField(max_length=30, primary_key=True)  # 编码
    name = models.CharField(max_length=100, null=True)  # 名称
    format = models.CharField(max_length=20, null=True)  #
    unit = models.CharField(max_length=20, null=True)  #
    price = models.FloatField(default=0)  # 单价
    note = models.CharField(max_length=220, null=True)  #
    create_date = models.CharField(max_length=20, null=True)  #
    create_user = models.CharField(max_length=20, null=True)  #
    status = models.BooleanField(default=True)  # 状态是否停用
class Stock(models.Model):  #库存明细表
    item_code = models.CharField(max_length=20,primary_key=True)  #SKU编码作为主键
    item_name = models.CharField(max_length=200)
    format = models.CharField(max_length=20, null=True)  #
    unit = models.CharField(max_length=20, null=True)  #
    stock_num = models.IntegerField(default=0,null=True)  # 库存数量
