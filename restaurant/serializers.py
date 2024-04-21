from rest_framework import serializers
from .models import *
from django.contrib import auth
from django.contrib.auth.models import User
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','title']


class MenuItemSerializer(serializers.ModelSerializer):
    # category = serializers.PrimaryKeyRelatedField(
    #    queryset=Category.objects.all())
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = MenuItem
        fields = ['id','title','price','featured','category','category_id']
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=MenuItem.objects.all(),
        #         fields=['title', 'category_id']
        #     )
        # ]
        # extra_kwargs = {
        #     'price': {
        #         'min_value': 1.0
        #     },
        #     'title': {
        #         'validators': [
        #             UniqueValidator(
        #                 queryset=MenuItem.objects.all()
        #             )
        #         ],
        #         'max_length': 150
        #     }
        # }

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'name', 'no_of_guests', 'booking_date']
 

class UserSerializer(serializers.ModelSerializer):
    # Date_Joined = serializers.SerializerMethodField()
    # date_joined = serializers.DateTimeField(write_only=True, default=datetime.now)
    # email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = ['id','username','email']
        # fields = ['id', 'username', 'email', 'date_joined', 'Date_Joined']
    #     extra_kwargs = {
    #         'email': {'read_only':True}
    #     }
    # def get_Date_Joined(self, obj):
    #     return obj.date_joined.strftime('%Y-%m-%d')

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','password']
    
    def create(self, validated_data):
        user = auth.authenticate(username = validated_data['username'],password = validated_data['password'])
        return user


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        try:
            user.set_password(validated_data['password'])
            user.save()
        except KeyError:
            pass
        return user


class CartSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(
    #         queryset=User.objects.all(),
    #         default=serializers.CurrentUserDefault()
    #     )
    # user = UserSerializer(read_only=True)
    # user_id = serializers.IntegerField(write_only=True)
    menuitem= MenuItemSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Cart
        fields = ['id','user','user_id','menuitem','quantity','unit_price', 'price','menuitem_id']
        
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Cart.objects.all(),
        #         fields = ['menuitem_id', 'user_id']
        #     )
        # ]
        # extra_kwargs = {
        #     'quantity': {
        #         'min_value': 0,
        #     },
        #     'unit_price': {
        #         'min_value': 0.0
        #     },
        #     'price': {
        #         'min_value': 0.0,
        #         'read_only': True
        #     },
        # }
        

class OrderSerializer(serializers.ModelSerializer):
    # orderitem = OrderItemSerializer(many=True, read_only=True, source='order')

    class Meta:
        model = Order
        fields = ['id','user','delivery_crew','status','total','date']
        # fields = ['id', 'user', 'delivery_crew', 'status', 'date', 'total', 'orderitem']
        validators = [
            UniqueTogetherValidator(
                queryset=Order.objects.all(),
                fields=['user', 'delivery_crew']
            )
        ]

        extra_kwargs = {
            'total': {'min_value': 0},
        }


class OrderItemSerializer(serializers.ModelSerializer):
    order= OrderSerializer(read_only=True)
    order_id = serializers.IntegerField(write_only=True)
    menuitem= MenuItemSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = OrderItem
        fields = ['id','order','order_id','menuitem','menuitem_id','quantity','price']
        
        depth = 1
        extra_kwargs = {
            'quantity': {
                'min_value': 0,
            },
            'price': {
                'min_value': 0.0
            },
        }