# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
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
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
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


class BlogBlogmodel(models.Model):
    title = models.CharField(max_length=120)
    slug = models.CharField(unique=True, max_length=50)
    description = models.TextField()
    image = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'blog_blogmodel'


class CatSub(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    rus_name = models.CharField(max_length=255, blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)
    c_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cat_sub'


class CatSubBack(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    rus_name = models.CharField(max_length=255, blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)
    c_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cat_sub_back'


class CatSubRus(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    rus_name = models.CharField(max_length=255, blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)
    c_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cat_sub_rus'


class CatSubTmp(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    rus_name = models.CharField(max_length=255, blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)
    c_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cat_sub_tmp'


class Categories(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    rus_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'categories'


class Categoryzacia(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    list_category_name = models.TextField(blank=True, null=True)
    list_category_href = models.TextField(blank=True, null=True)
    rus_name = models.CharField(max_length=255)
    parent_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categoryzacia'


class CategoryzaciaBack(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    list_category_name = models.TextField(blank=True, null=True)
    list_category_href = models.TextField(blank=True, null=True)
    rus_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'categoryzacia_back'


class DataTest(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    href = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    price = models.CharField(max_length=255, blank=True, null=True)
    subcat = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    id_p = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_test'


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


class MainTable(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    car = models.CharField(max_length=100, blank=True, null=True)
    car_model = models.CharField(max_length=100, blank=True, null=True)
    car_year = models.CharField(max_length=100, blank=True, null=True)
    volume = models.CharField(max_length=100, blank=True, null=True)
    horse_power = models.CharField(max_length=100)
    engine_code = models.CharField(max_length=100, blank=True, null=True)
    cat_number = models.CharField(max_length=100, blank=True, null=True)
    price = models.CharField(max_length=100, blank=True, null=True)
    distance = models.CharField(max_length=100, blank=True, null=True)
    weight = models.CharField(max_length=100, blank=True, null=True)
    supplier_id = models.CharField(max_length=100, blank=True, null=True)
    notice = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'main_table'


class OrmAlbum(models.Model):
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    num_stars = models.IntegerField()
    artist = models.ForeignKey('OrmMusician', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'orm_album'


class OrmAuthor(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=254)

    class Meta:
        managed = False
        db_table = 'orm_author'


class OrmBlog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    class Meta:
        managed = False
        db_table = 'orm_blog'


class OrmEntry(models.Model):
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    n_comments = models.IntegerField()
    n_pingbacks = models.IntegerField()
    rating = models.IntegerField()
    blog = models.ForeignKey(OrmBlog, models.DO_NOTHING)
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'orm_entry'


class OrmEntryAuthors(models.Model):
    entry = models.ForeignKey(OrmEntry, models.DO_NOTHING)
    author = models.ForeignKey(OrmAuthor, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'orm_entry_authors'
        unique_together = (('entry', 'author'),)


class OrmMusician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    instrument = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'orm_musician'


class OrmPerson(models.Model):
    name = models.CharField(max_length=60)
    shirt_size = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'orm_person'


class OrmPizza(models.Model):

    class Meta:
        managed = False
        db_table = 'orm_pizza'


class OrmPizzaToppings(models.Model):
    pizza = models.ForeignKey(OrmPizza, models.DO_NOTHING)
    topping = models.ForeignKey('OrmTopping', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'orm_pizza_toppings'
        unique_together = (('pizza', 'topping'),)


class OrmTopping(models.Model):

    class Meta:
        managed = False
        db_table = 'orm_topping'


class ProductCategoryzacia(models.Model):
    list_category_href = models.TextField(blank=True, null=True)
    list_category_name = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=500, blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    rus_name = models.CharField(max_length=500, blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_categoryzacia'


class ProductCatsubrus(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    rus_name = models.CharField(max_length=255, blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)
    old_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_catsubrus'


class ProductProduct(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(max_digits=20, decimal_places=2)
    image = models.CharField(max_length=100, blank=True, null=True)
    featured = models.IntegerField()
    slug = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'product_product'


class Suppliers(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    avalibilty = models.IntegerField()
    tel = models.CharField(max_length=17)
    term = models.IntegerField()
    supply_condition = models.CharField(max_length=100)
    notes = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=100)
    currency = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'suppliers'
