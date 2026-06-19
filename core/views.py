"""Представления (views) сайта ресторана."""
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookingForm, FeedbackForm
from .models import Category, Dish, News


def home(request):
    """Главная страница: приветствие, краткая информация, последние новости."""
    latest_news = News.objects.filter(is_active=True).order_by('-published_at')[:3]
    featured_dishes = Dish.objects.filter(is_available=True).select_related('category')[:6]
    return render(request, 'core/home.html', {
        'latest_news': latest_news,
        'featured_dishes': featured_dishes,
    })


def menu(request):
    """Меню с фильтрацией по категории, цене и поиском по названию."""
    dishes = Dish.objects.filter(is_available=True).select_related('category')

    category_slug = request.GET.get('category', '').strip()
    if category_slug:
        dishes = dishes.filter(category__slug=category_slug)

    price_min_raw = request.GET.get('price_min', '').strip()
    price_max_raw = request.GET.get('price_max', '').strip()

    price_min = _parse_decimal(price_min_raw)
    price_max = _parse_decimal(price_max_raw)
    if price_min is not None:
        dishes = dishes.filter(price__gte=price_min)
    if price_max is not None:
        dishes = dishes.filter(price__lte=price_max)

    query = request.GET.get('q', '').strip()
    if query:
        dishes = dishes.filter(name__icontains=query)

    categories = Category.objects.all()

    return render(request, 'core/menu.html', {
        'dishes': dishes,
        'categories': categories,
        'selected_category': category_slug,
        'query': query,
        'price_min': price_min_raw,
        'price_max': price_max_raw,
    })


def _parse_decimal(value):
    """Безопасный парсинг строки в Decimal. Возвращает None при ошибке."""
    if not value:
        return None
    try:
        result = Decimal(value.replace(',', '.'))
    except (InvalidOperation, ValueError):
        return None
    if result < 0:
        return None
    return result


def booking(request):
    """Страница онлайн-бронирования столика."""
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Столик забронирован. Мы свяжемся с вами для подтверждения.')
            return redirect('booking')
        else:
            messages.error(request, 'Проверьте корректность заполнения формы.')
    else:
        form = BookingForm()
    return render(request, 'core/booking.html', {'form': form})


def feedback(request):
    """Страница обратной связи."""
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Сообщение отправлено. Спасибо за обратную связь!')
            return redirect('feedback')
        else:
            messages.error(request, 'Проверьте корректность заполнения формы.')
    else:
        form = FeedbackForm()
    return render(request, 'core/feedback.html', {'form': form})


def news_list(request):
    """Список активных новостей."""
    items = News.objects.filter(is_active=True).order_by('-published_at')
    return render(request, 'core/news_list.html', {'news_items': items})


def news_detail(request, pk):
    """Страница одной новости."""
    item = get_object_or_404(News, pk=pk, is_active=True)
    return render(request, 'core/news_detail.html', {'item': item})


def about(request):
    """Страница «О ресторане»."""
    return render(request, 'core/about.html')
