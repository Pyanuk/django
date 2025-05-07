from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Categories, Users, Products, Cart, Orders, OrderItems
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
import json
from django.core.mail import send_mail
from django.conf import settings

def home(request):
    return render(request, 'home/index.html')

def company(request):
    return render(request, 'home/company.html')

def contacts(request):
    return render(request, 'home/contacts.html')

def map(request):
    return render(request, 'home/map.html')

def category(request):
    return render(request, 'home/category.html')

def full(request):
    products = Products.objects.all()
    
    
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(name__icontains=search_query)
    
      
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    else:
        products = products.order_by('name')
    
    categories = Categories.objects.all()
    cart_items = []


    if 'user_id' in request.session:
        user = Users.objects.get(id=request.session['user_id'])
        cart_items = Cart.objects.filter(user=user).values_list('product_id', flat=True)

    return render(request, 'home/fullproducts.html', {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'cart_items': cart_items 
    })

def basket(request):
    if 'user_id' not in request.session:
        messages.error(request, 'Чтобы посмотреть корзину, нужно авторизоваться.')
        return redirect('login')

    cart_items_with_total = []
    total = 0
    user = Users.objects.get(id=request.session['user_id'])
    cart_items = Cart.objects.filter(user=user)
    total = sum(item.product.price * item.quantity for item in cart_items)
    cart_items_with_total = [{'item': item, 'subtotal': item.product.price * item.quantity} for item in cart_items]

    return render(request, 'home/basket.html', {'cart_items': cart_items_with_total, 'total': total})

def add_to_cart(request, product_id):
    if 'user_id' not in request.session:
        return JsonResponse({
            'success': False,
            'error': 'Вы должны авторизоваться, чтобы добавить товар в корзину.'
        })
    
    try:
        user = Users.objects.get(id=request.session['user_id'])
        product = Products.objects.get(id=product_id)
        cart_item, created = Cart.objects.get_or_create(user=user, product=product, defaults={'quantity': 1})
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return JsonResponse({
            'success': True,
            'message': 'Товар добавлен в корзину!',
            'product_id': product_id,
            'in_cart': True
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

def update_cart(request, cart_id):
    if 'user_id' not in request.session:
        messages.error(request, 'Вы должны авторизоваться, чтобы изменить корзину.')
        return redirect('login')
    
    cart_item = Cart.objects.get(id=cart_id, user_id=request.session['user_id'])
    action = request.GET.get('action')
    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()
        return redirect('basket')
    elif action == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        return redirect('basket')
    elif action == 'delete':
        product_id = cart_item.product.id
        cart_item.delete()
        return JsonResponse({
            'success': True,
            'product_id': product_id,
            'in_cart': False
        })
    return redirect('basket')

def register(request):
    if request.method == 'POST':
        surname = request.POST['surname']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        
        if Users.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('register')
        
        if Users.objects.filter(phone=phone).exists():
            messages.error(request, 'Phone number already exists.')
            return redirect('register')
        
        user = Users(
            surname=surname,
            name=name,
            email=email,
            phone=phone,
            password_users=make_password(password)
        )
        user.save()
        messages.success(request, 'Registration successful. Please log in.')
        return redirect('login')
    return render(request, 'auth/registration.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        try:
            user = Users.objects.get(email=email)
            if check_password(password, user.password_users):
                request.session['user_id'] = user.id
                messages.success(request, 'Logged in successfully.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password.')
                return redirect('login')
        except Users.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
            return redirect('login')
    return render(request, 'auth/login.html')

def user_logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    messages.success(request, 'Logged out successfully.')
    return redirect('login')

def categories_view(request):
    categories = Categories.objects.all()
    cart_items = []

    if 'user_id' in request.session:
        user = Users.objects.get(id=request.session['user_id'])
        cart_items = Cart.objects.filter(user=user).values_list('product_id', flat=True)

    return render(request, 'home/category.html', {
        'categories': categories,
        'cart_items': cart_items 
    })

@require_POST
@csrf_exempt  
def checkout(request):
    if 'user_id' not in request.session:
        return JsonResponse({'success': False, 'error': 'Вы должны авторизоваться.'})

    try:
        data = json.loads(request.body)
        user = Users.objects.get(id=request.session['user_id'])
        email = data.get('email')  
        total_amount = float(data.get('total_amount', 0))

        if not email:
            return JsonResponse({'success': False, 'error': 'Пожалуйста, укажите email.'})

        order = Orders.objects.create(
            user=user,
            order_date=timezone.now(),
            payment_method=data.get('payment_method', 'credit_card'),
            total_amount=total_amount
        )

        cart_items = Cart.objects.filter(user=user)
        order_details = []
        for item in cart_items:
            OrderItems.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            order_details.append(f"- {item.product.name}: {item.quantity} шт. x {item.product.price} ₽ = {item.quantity * item.product.price} ₽")
        
        order_details_str = "\n".join(order_details)
        message = f"""Здравствуйте!\n
Ваш заказ успешно оформлен.\n
Детали заказа:\n{order_details_str}\n
Итоговая сумма: {total_amount} ₽\n
Спасибо за покупку!\n
С уважением,\nКоманда Pyanuk Store"""

        send_mail(
            subject='Подтверждение заказа',
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False
        )

        # Удаляем товары из корзины
        cart_items.delete()

        return JsonResponse({'success': True, 'message': 'Заказ успешно оформлен!'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})