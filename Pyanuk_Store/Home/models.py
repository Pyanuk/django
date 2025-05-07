from django.db import models
from django.core.validators import MinValueValidator

MAX_LENGTH = 255  # Общая длина для строковых полей

class Users(models.Model):
    surname = models.CharField(max_length=50, verbose_name='Фамилия')
    name = models.CharField(max_length=50, verbose_name='Имя')
    email = models.EmailField(max_length=100, unique=True, verbose_name='Email')
    phone = models.CharField(max_length=20, unique=True, verbose_name='Телефон')
    password_users = models.CharField(max_length=200, verbose_name='Пароль')

    def __str__(self):
        return f"{self.name} {self.surname}"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Categories(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, unique=True, verbose_name='Название категории')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Manufacturers(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, unique=True, verbose_name='Наименование производителя')
    country = models.CharField(max_length=MAX_LENGTH, unique=True, verbose_name='Страна')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'


class Products(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Название товара')
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, verbose_name='Категория')
    manufacturer = models.ForeignKey(Manufacturers, on_delete=models.CASCADE, verbose_name='Производитель')
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name='Цена')
    stock_quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)], verbose_name='Количество на складе')
    image_url = models.CharField(max_length=MAX_LENGTH, null=True, blank=True, verbose_name='Изображение')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Cart(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.IntegerField(validators=[MinValueValidator(1)], verbose_name='Количество')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class Favorites(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='Товар')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'


class Orders(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='Пользователь')
    order_date = models.DateTimeField(verbose_name='Дата заказа')
    payment_method = models.CharField(max_length=100, verbose_name='Метод оплаты')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая сумма')

    def __str__(self):
        return f"Заказ #{self.pk}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItems(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.IntegerField(verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за единицу')

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'
