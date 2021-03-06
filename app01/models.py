# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TAddress(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40)
    detail_address = models.CharField(max_length=40)
    zipcode = models.CharField(max_length=20)
    telphone = models.CharField(max_length=40, blank=True, null=True)
    addr_mobile = models.CharField(max_length=40, blank=True, null=True)
    user = models.ForeignKey('TUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 't_address'


class TBook(models.Model):
    book_id = models.IntegerField(primary_key=True)
    book_name = models.CharField(max_length=128, blank=True, null=True)
    book_author = models.CharField(max_length=64, blank=True, null=True)
    book_publish = models.CharField(max_length=128, blank=True, null=True)
    publish_time = models.DateField(blank=True, null=True)
    revision = models.IntegerField(blank=True, null=True)
    book_isbn = models.CharField(max_length=64, blank=True, null=True)
    word_count = models.CharField(max_length=64, blank=True, null=True)
    page_count = models.IntegerField(blank=True, null=True)
    book_paper = models.CharField(max_length=64, blank=True, null=True)
    book_wrapper = models.CharField(max_length=64, blank=True, null=True)
    book_category = models.ForeignKey('TCategory', models.DO_NOTHING, db_column='book_category', blank=True, null=True)
    book_price = models.FloatField(blank=True, null=True)
    book_dprice = models.FloatField(blank=True, null=True)
    series_name = models.CharField(max_length=64, blank=True, null=True)
    printing_time = models.DateField(blank=True, null=True)
    impression = models.CharField(max_length=64, blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    shelves_date = models.DateField(blank=True, null=True)
    customer_socre = models.CharField(max_length=64, blank=True, null=True)
    book_status = models.CharField(max_length=64, blank=True, null=True)
    sales = models.CharField(max_length=64, blank=True, null=True)
    book_pic = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_book'


class TCategory(models.Model):
    idcategory_id = models.IntegerField(primary_key=True)
    category_name = models.CharField(max_length=40)
    book_counts = models.CharField(max_length=40, blank=True, null=True)
    category_pid = models.IntegerField()#max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_category'


class TOrder(models.Model):
    id = models.IntegerField(primary_key=True)
    num = models.CharField(max_length=40, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    order_addrid = models.ForeignKey(TAddress, models.DO_NOTHING, db_column='order_addrid')
    order_uid = models.ForeignKey('TUser', models.DO_NOTHING, db_column='order_uid')
    status = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_order'


class TOrderitem(models.Model):
    shop_id = models.IntegerField(primary_key=True)
    shop_ordid = models.ForeignKey(TOrder, models.DO_NOTHING, db_column='shop_ordid')
    shop_bookid = models.ForeignKey(TBook, models.DO_NOTHING, db_column='shop_bookid')
    shop_num = models.CharField(max_length=40)
    total_price = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_orderitem'


class TUser(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_email = models.EmailField()
    user_name = models.CharField(max_length=40)#, blank=True, null=True)
    user_password = models.CharField(max_length=40)#, blank=True, null=True)
    user_status = models.CharField(max_length=40)#, blank=True, null=True)
    # c_time = models.DateTimeField(auto_now_add=True)
    # has_confirm = models.BooleanField(default=False, verbose_name='是否确认')

    class Meta:
        # managed = False
        db_table = 't_user'
#
class Confirm_string(models.Model):
    code = models.CharField(max_length=256, verbose_name='用户注册码')
    user = models.ForeignKey('TUser', on_delete=models.CASCADE, verbose_name='关联的用户')
    code_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 't_confirm_string'