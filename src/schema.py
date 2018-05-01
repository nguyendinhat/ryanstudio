# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('TaikhoanThanhvien', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class TaikhoanBophan(models.Model):
    id_bophan = models.AutoField(primary_key=True)
    ten_bophan = models.CharField(max_length=255, blank=True, null=True)
    mota = models.TextField()

    class Meta:
        managed = False
        db_table = 'taikhoan_bophan'


class TaikhoanKhach(models.Model):
    id_khach = models.AutoField(primary_key=True)
    email = models.CharField(max_length=254)
    is_active = models.IntegerField()
    update = models.DateTimeField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'taikhoan_khach'


class TaikhoanThanhvien(models.Model):
    id_thanhvien = models.AutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    email = models.CharField(unique=True, max_length=255)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    ngaysinh = models.DateField(blank=True, null=True)
    gioitinh = models.CharField(max_length=9)
    sdt = models.CharField(max_length=11)
    is_active = models.IntegerField()
    is_staff = models.IntegerField()
    is_admin = models.IntegerField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'taikhoan_thanhvien'


class TaikhoanThanhvienbophan(models.Model):
    is_active = models.IntegerField()
    id_bophan = models.ForeignKey(TaikhoanBophan, models.DO_NOTHING)
    id_thanhvien = models.ForeignKey(TaikhoanThanhvien, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'taikhoan_thanhvienbophan'
        unique_together = (('id_thanhvien', 'id_bophan'),)
