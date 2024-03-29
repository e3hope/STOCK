from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

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


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Board(models.Model):
    idx = models.AutoField(primary_key=True)
    id = models.CharField(max_length=30)
    code = models.CharField(max_length=20)
    contents = models.CharField(max_length=200)
    date_insert = models.DateTimeField(blank=True, null=True)
    date_update = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'board'


class BookmarkGroup(models.Model):
    idx = models.AutoField(primary_key=True)
    id = models.CharField(max_length=30, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    date_insert = models.DateTimeField(blank=True, null=True)
    date_update = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bookmark_group'


class BookmarkStock(models.Model):
    idx = models.AutoField(primary_key=True)
    group_idx = models.IntegerField(blank=True, null=True)
    code = models.CharField(max_length=20, blank=True, null=True)
    date_insert = models.DateTimeField(blank=True, null=True)
    id = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'bookmark_stock'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
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


class Krx(models.Model):
    idx = models.AutoField(primary_key=True)    
    code = models.CharField(max_length=1024, blank=True, null=True)
    name = models.CharField(db_column='Name', max_length=1024, blank=True, null=True)  # Field name made lowercase.
    market = models.CharField(max_length=1024, blank=True, null=True)
    dept = models.CharField(max_length=1024, blank=True, null=True)
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    changecode = models.IntegerField(blank=True, null=True)
    changes = models.FloatField(blank=True,null=True)
    chagesratio = models.FloatField(blank=True, null=True)
    open = models.FloatField(db_column='Open', blank=True, null=True)  # Field name made lowercase.
    high = models.FloatField(blank=True, null=True)
    low = models.FloatField(blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    marcap = models.FloatField(blank=True, null=True)
    stocks = models.FloatField(blank=True, null=True)
    marketid = models.CharField(max_length=1024, blank=True, null=True)
    rank = models.IntegerField(db_column='Rank', blank=True, null=True)  # Field name made lowercase.
    date = models.CharField(db_column='Date', max_length=1024, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'krx'


class MockInvestment(models.Model):
    idx = models.AutoField(primary_key=True)
    id = models.CharField(max_length=30, blank=True, null=True)
    code = models.CharField(max_length=20, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    date_insert = models.DateTimeField(blank=True, null=True)
    date_update = models.DateTimeField(blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mock_investment'


class MockOrder(models.Model):
    idx = models.AutoField(primary_key=True)
    id = models.CharField(max_length=30, blank=True, null=True)
    code = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    date_check = models.CharField(max_length=30, blank=True, null=True)
    date_insert = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mock_order'


class News(models.Model):
    idx = models.AutoField(primary_key=True)
    company = models.CharField(max_length=20, blank=True, null=True)
    title = models.CharField(max_length=80, blank=True, null=True)
    text = models.CharField(max_length=1000, blank=True, null=True)
    date = models.CharField(max_length=20, blank=True, null=True)
    img = models.CharField(max_length=200, blank=True, null=True)
    href = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'news'


class Stock(models.Model):
    idx = models.AutoField(primary_key=True)
    code = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock'


class User(models.Model):
    idx = models.AutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=30)
    password = models.TextField()
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    date_insert = models.DateTimeField(blank=True, null=True)
    date_update = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class UserCapital(models.Model):
    idx = models.AutoField(primary_key=True)
    id = models.CharField(max_length=30)
    capital = models.IntegerField(blank=True, null=True)
    date_check = models.CharField(max_length=30, blank=True, null=True)
    date_insert = models.DateTimeField(blank=True, null=True)
    date_update = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_capital'


class Word(models.Model):
    idx = models.AutoField(primary_key=True)
    word = models.CharField(max_length=30)
    mean = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'word'