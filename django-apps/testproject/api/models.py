# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
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


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

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
    id = models.BigAutoField(primary_key=True)
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


class RegisterValuesEm6400(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    tot_active_energy = models.FloatField(blank=True, null=True)
    i_a = models.FloatField(blank=True, null=True)
    i_b = models.FloatField(blank=True, null=True)
    i_c = models.FloatField(blank=True, null=True)
    i_avg = models.FloatField(blank=True, null=True)
    v_ab = models.FloatField(blank=True, null=True)
    v_bc = models.FloatField(blank=True, null=True)
    v_ca = models.FloatField(blank=True, null=True)
    v_ll_avg = models.FloatField(blank=True, null=True)
    v_an = models.FloatField(blank=True, null=True)
    v_bn = models.FloatField(blank=True, null=True)
    v_cn = models.FloatField(blank=True, null=True)
    v_ln_avg = models.FloatField(blank=True, null=True)
    active_pow_a = models.FloatField(blank=True, null=True)
    active_pow_b = models.FloatField(blank=True, null=True)
    active_pow_c = models.FloatField(blank=True, null=True)
    active_power_tot = models.FloatField(blank=True, null=True)
    pf_a = models.FloatField(blank=True, null=True)
    pf_b = models.FloatField(blank=True, null=True)
    pf_c = models.FloatField(blank=True, null=True)
    pf_tot = models.FloatField(blank=True, null=True)
    frequency = models.FloatField(blank=True, null=True)
    thd_i_a = models.FloatField(blank=True, null=True)
    thd_i_b = models.FloatField(blank=True, null=True)
    thd_i_c = models.FloatField(blank=True, null=True)
    thd_v_an = models.FloatField(blank=True, null=True)
    thd_v_bn = models.FloatField(blank=True, null=True)
    thd_v_cn = models.FloatField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    deviceid = models.PositiveIntegerField(db_column='deviceId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'register_values_em6400'


class RegisterValuesEn6400Ng(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    active_energy_del_in = models.FloatField(blank=True, null=True)
    active_energy_rec_out = models.FloatField(blank=True, null=True)
    i_a = models.FloatField(blank=True, null=True)
    i_b = models.FloatField(blank=True, null=True)
    i_c = models.FloatField(blank=True, null=True)
    i_n = models.FloatField(blank=True, null=True)
    i_g = models.FloatField(blank=True, null=True)
    i_avg = models.FloatField(blank=True, null=True)
    v_ab = models.FloatField(blank=True, null=True)
    v_bc = models.FloatField(blank=True, null=True)
    v_ca = models.FloatField(blank=True, null=True)
    v_ll_avg = models.FloatField(blank=True, null=True)
    v_an = models.FloatField(blank=True, null=True)
    v_bn = models.FloatField(blank=True, null=True)
    v_cn = models.FloatField(blank=True, null=True)
    v_ln_avg = models.FloatField(blank=True, null=True)
    active_pow_a = models.FloatField(blank=True, null=True)
    active_pow_b = models.FloatField(blank=True, null=True)
    active_pow_c = models.FloatField(blank=True, null=True)
    active_power_tot = models.FloatField(blank=True, null=True)
    pf_a = models.FloatField(blank=True, null=True)
    pf_b = models.FloatField(blank=True, null=True)
    pf_c = models.FloatField(blank=True, null=True)
    pf_tot = models.FloatField(blank=True, null=True)
    frequency = models.FloatField(blank=True, null=True)
    thd_i_a = models.FloatField(blank=True, null=True)
    thd_i_b = models.FloatField(blank=True, null=True)
    thd_i_c = models.FloatField(blank=True, null=True)
    thd_i_n = models.FloatField(blank=True, null=True)
    thd_i_g = models.FloatField(blank=True, null=True)
    thd_v_ab = models.FloatField(blank=True, null=True)
    thd_v_bc = models.FloatField(blank=True, null=True)
    thd_v_ca = models.FloatField(blank=True, null=True)
    thd_v_ll = models.FloatField(blank=True, null=True)
    thd_v_an = models.FloatField(blank=True, null=True)
    thd_v_bn = models.FloatField(blank=True, null=True)
    thd_v_cn = models.FloatField(blank=True, null=True)
    thd_v_ln = models.FloatField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    deviceid = models.PositiveIntegerField(db_column='deviceId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'register_values_en6400ng'
