"""Модели данных сайта ресторана «Старик и море»."""
from django.db import models
from django.utils import timezone


class Category(models.Model):
    """Категория блюд (например: Закуски, Горячее, Напитки)."""

    name = models.CharField('Название', max_length=100, unique=True)
    slug = models.SlugField('Идентификатор (URL)', max_length=120, unique=True)
    order = models.PositiveIntegerField('Порядок отображения', default=0)

    class Meta:
        verbose_name = 'Категория меню'
        verbose_name_plural = 'Категории меню'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Dish(models.Model):
    """Блюдо в меню ресторана."""

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='dishes',
        verbose_name='Категория',
    )
    name = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    price = models.DecimalField('Цена, ₽', max_digits=8, decimal_places=2)
    image = models.ImageField('Фото', upload_to='dishes/', blank=True, null=True)
    is_available = models.BooleanField('Доступно в меню', default=True)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'
        ordering = ['category__order', 'name']

    def __str__(self):
        return f'{self.name} ({self.category.name})'


class News(models.Model):
    """Новость ресторана."""

    title = models.CharField('Заголовок', max_length=200)
    content = models.TextField('Текст новости')
    image = models.ImageField('Изображение', upload_to='news/', blank=True, null=True)
    is_active = models.BooleanField('Опубликовано', default=True)
    published_at = models.DateTimeField('Дата публикации', default=timezone.now)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-published_at']

    def __str__(self):
        return self.title


class Booking(models.Model):
    """Заявка на бронирование столика."""

    STATUS_NEW = 'new'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_NEW, 'Новая'),
        (STATUS_CONFIRMED, 'Подтверждена'),
        (STATUS_CANCELLED, 'Отменена'),
    ]

    name = models.CharField('Имя гостя', max_length=100)
    phone = models.CharField('Телефон', max_length=20)
    date = models.DateField('Дата')
    time = models.TimeField('Время')
    guests = models.PositiveSmallIntegerField('Количество гостей')
    note = models.TextField('Примечание', blank=True)
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
    )
    created_at = models.DateTimeField('Дата заявки', auto_now_add=True)

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
        ordering = ['-date', '-time']

    def __str__(self):
        return f'{self.name} — {self.date} {self.time:%H:%M}'


class Feedback(models.Model):
    """Сообщение от посетителя через форму обратной связи."""

    name = models.CharField('Имя', max_length=100)
    email = models.EmailField('E-mail')
    message = models.TextField('Сообщение')
    is_read = models.BooleanField('Прочитано', default=False)
    created_at = models.DateTimeField('Дата отправки', auto_now_add=True)

    class Meta:
        verbose_name = 'Сообщение обратной связи'
        verbose_name_plural = 'Обратная связь'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.email})'
