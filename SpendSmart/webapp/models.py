# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Attachment(models.Model):
    attachmentid = models.AutoField(db_column='attachmentId', primary_key=True)  # Field name made lowercase.
    attachmentblob = models.TextField(db_column='attachmentBlob', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Attachment'


class Borrows(models.Model):
    borrowerid = models.OneToOneField('User', models.DO_NOTHING, db_column='borrowerId', primary_key=True)  # Field name made lowercase. The composite primary key (borrowerId, splitId) found, that is not supported. The first column is selected.
    splitid = models.ForeignKey('Split', models.DO_NOTHING, db_column='splitId')  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=10, decimal_places=2)  # Field name made lowercase.
    ispaid = models.IntegerField(db_column='isPaid')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Borrows'
        unique_together = (('borrowerid', 'splitid'),)


class Category(models.Model):
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    categoryid = models.AutoField(db_column='categoryId', primary_key=True)  # Field name made lowercase.
    parentcategoryid = models.ForeignKey('self', models.DO_NOTHING, db_column='parentCategoryId', blank=True, null=True)  # Field name made lowercase.
    categoryname = models.CharField(db_column='categoryName', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Category'
    


class Credentials(models.Model):
    email = models.CharField(primary_key=True, max_length=255)
    password = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'Credentials'


class Monthlycategorybudget(models.Model):
    budgetid = models.AutoField(db_column='budgetId', primary_key=True)  # Field name made lowercase.
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DateField()
    categoryid = models.ForeignKey(Category, models.DO_NOTHING, db_column='categoryId')  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MonthlyCategoryBudget'


class Split(models.Model):
    splitid = models.AutoField(db_column='splitId', primary_key=True)  # Field name made lowercase.
    title = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(blank=True, null=True)
    lenderid = models.ForeignKey('User', models.DO_NOTHING, db_column='lenderId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Split'


class Transaction(models.Model):
    txnid = models.AutoField(db_column='txnId', primary_key=True)  # Field name made lowercase.
    title = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(blank=True, null=True)
    paymentmethod = models.CharField(db_column='paymentMethod', max_length=255, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(max_length=255)
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    attachmentid = models.ForeignKey(Attachment, models.DO_NOTHING, db_column='attachmentId', blank=True, null=True)  # Field name made lowercase.
    categoryid = models.ForeignKey(Category, models.DO_NOTHING, db_column='categoryId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Transaction'


class User(models.Model):
    userid = models.AutoField(db_column='userId', primary_key=True)  # Field name made lowercase.
    username = models.CharField(db_column='userName', max_length=255)  # Field name made lowercase.
    firstname = models.CharField(db_column='firstName', max_length=255)  # Field name made lowercase.
    lastname = models.CharField(db_column='lastName', max_length=255)  # Field name made lowercase.
    email = models.ForeignKey(Credentials, models.DO_NOTHING, db_column='email')

    class Meta:
        managed = False
        db_table = 'User'
    def __str__(self):
        return self.email
    
# models.py

from django.db import models

class Expense(models.Model):
    TYPE_CHOICES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )

    CATEGORY_CHOICES = (
        ('category1', 'Category 1'),
        ('category2', 'Category 2'),
        # Add more categories as needed
    )

    PAYMENT_METHOD_CHOICES = (
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('bank_transfer', 'Bank Transfer'),
        # Add more payment methods as needed
    )

    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    note = models.TextField(blank=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)

    def __str__(self):
        return self.description

# class Expense(models.Model):
#     TYPE_CHOICES = (
#         ('income', 'Income'),
#         ('expense', 'Expense'),
#     )

#     CATEGORY_CHOICES = (
#         ('category1', 'Category 1'),
#         ('category2', 'Category 2'),
#         # Add more categories as needed
#     )

#     PAYMENT_METHOD_CHOICES = (
#         ('cash', 'Cash'),
#         ('credit_card', 'Credit Card'),
#         ('debit_card', 'Debit Card'),
#         ('bank_transfer', 'Bank Transfer'),
#         # Add more payment methods as needed
#     )

#     description = models.TextField()
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     date = models.DateField()
#     type = models.CharField(max_length=10, choices=TYPE_CHOICES)
#     category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
#     note = models.TextField(blank=True)
#     payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)

#     def __str__(self):
#         return self.description

# class AuthGroup(models.Model):
#     name = models.CharField(unique=True, max_length=150)

#     class Meta:
#         managed = False
#         db_table = 'auth_group'


# class AuthGroupPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#     permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'auth_group_permissions'
#         unique_together = (('group', 'permission'),)


# class AuthPermission(models.Model):
#     name = models.CharField(max_length=255)
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
#     codename = models.CharField(max_length=100)

#     class Meta:
#         managed = False
#         db_table = 'auth_permission'
#         unique_together = (('content_type', 'codename'),)


# class AuthUser(models.Model):
#     password = models.CharField(max_length=128)
#     last_login = models.DateTimeField(blank=True, null=True)
#     is_superuser = models.IntegerField()
#     username = models.CharField(unique=True, max_length=150)
#     first_name = models.CharField(max_length=150)
#     last_name = models.CharField(max_length=150)
#     email = models.CharField(max_length=254)
#     is_staff = models.IntegerField()
#     is_active = models.IntegerField()
#     date_joined = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'auth_user'


# class AuthUserGroups(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'auth_user_groups'
#         unique_together = (('user', 'group'),)


# class AuthUserUserPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'auth_user_user_permissions'
#         unique_together = (('user', 'permission'),)


# class DjangoAdminLog(models.Model):
#     action_time = models.DateTimeField()
#     object_id = models.TextField(blank=True, null=True)
#     object_repr = models.CharField(max_length=200)
#     action_flag = models.PositiveSmallIntegerField()
#     change_message = models.TextField()
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'django_admin_log'


# class DjangoContentType(models.Model):
#     app_label = models.CharField(max_length=100)
#     model = models.CharField(max_length=100)

#     class Meta:
#         managed = False
#         db_table = 'django_content_type'
#         unique_together = (('app_label', 'model'),)


# class DjangoMigrations(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     app = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     applied = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'django_migrations'


# class DjangoSession(models.Model):
#     session_key = models.CharField(primary_key=True, max_length=40)
#     session_data = models.TextField()
#     expire_date = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'django_session'



