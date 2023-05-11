# Generated by Django 4.1.7 on 2023-04-14 11:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phone', models.IntegerField()),
                ('country', models.CharField(max_length=50)),
                ('address1', models.CharField(max_length=100)),
                ('address2', models.CharField(max_length=100)),
                ('landmark', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('pincode', models.IntegerField()),
                ('addresstype', models.CharField(max_length=20)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('email_verified', models.BooleanField(default=False)),
                ('user_status', models.CharField(max_length=20)),
                ('addressline1', models.CharField(max_length=100)),
                ('addressline2', models.CharField(max_length=100)),
                ('addressline3', models.CharField(max_length=100)),
                ('pin', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('pic', models.ImageField(blank=True, default=None, null=True, upload_to='images/')),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='MainCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('email_verified', models.BooleanField(default=False)),
                ('user_status', models.CharField(max_length=20)),
                ('addressline1', models.CharField(max_length=100)),
                ('addressline2', models.CharField(max_length=100)),
                ('addressline3', models.CharField(max_length=100)),
                ('pin', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('pic', models.ImageField(blank=True, default=None, null=True, upload_to='images/')),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShopProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('price', models.IntegerField()),
                ('discount', models.IntegerField()),
                ('promotion_price', models.IntegerField()),
                ('color', models.CharField(max_length=20)),
                ('size', models.CharField(max_length=20)),
                ('stock', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('pic1', models.ImageField(blank=True, default=None, null=True, upload_to='images/')),
                ('pic2', models.ImageField(blank=True, default=None, null=True, upload_to='images/')),
                ('pic3', models.ImageField(blank=True, default=None, null=True, upload_to='images/')),
                ('pic4', models.ImageField(blank=True, default=None, null=True, upload_to='images/')),
                ('date', models.DateTimeField(auto_now=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.brand')),
                ('mainCategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.maincategory')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.seller')),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.buyer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.shopproduct')),
            ],
        ),
        migrations.AddField(
            model_name='shopproduct',
            name='subCategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.subcategory'),
        ),
        migrations.CreateModel(
            name='SellerApproval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sellerstatus', models.CharField(blank=True, default='Requested', max_length=20, null=True)),
                ('aadharcard', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('pancard', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.buyer')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subtotal', models.IntegerField(blank=True, default=0, null=True)),
                ('shipping', models.IntegerField(blank=True, default=0, null=True)),
                ('ordertotal', models.IntegerField(blank=True, default=0, null=True)),
                ('paymentmethod', models.CharField(blank=True, default='COD', max_length=20, null=True)),
                ('paymentstatus', models.CharField(blank=True, default='Pending', max_length=20, null=True)),
                ('orderstatus', models.CharField(blank=True, default='Not Packed', max_length=20, null=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('rzppid', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('rzpoid', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('rzpsid', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.address')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.buyer')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.seller')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('q', models.IntegerField(default=1)),
                ('total', models.IntegerField(default=0)),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.payment')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.shopproduct')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('productid', models.IntegerField()),
                ('price', models.IntegerField()),
                ('promotion_price', models.IntegerField()),
                ('image', models.URLField()),
                ('quantity', models.IntegerField()),
                ('subtotal', models.IntegerField()),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.buyer')),
            ],
        ),
        migrations.AddField(
            model_name='address',
            name='buyer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.buyer'),
        ),
    ]
