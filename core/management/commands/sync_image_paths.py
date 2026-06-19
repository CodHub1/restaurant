"""Обновляет пути к изображениям после переименования файлов media/."""
from django.core.management.base import BaseCommand

from core.models import Dish, News

IMAGE_PATHS = {
    'dishes/Снимок_экрана_2026-05-29_165209.png': 'dishes/dish-1.png',
    'dishes/Снимок_экрана_2026-05-29_165642.png': 'dishes/dish-2.png',
    'dishes/Снимок_экрана_2026-05-29_170342.png': 'dishes/dish-3.png',
    'dishes/Снимок_экрана_2026-05-29_170846.png': 'dishes/dish-4.png',
    'dishes/Снимок_экрана_2026-05-29_171605.png': 'dishes/dish-5.png',
    'dishes/Снимок_экрана_2026-05-29_172528.png': 'dishes/dish-6.png',
    'dishes/Снимок_экрана_2026-06-07_172122.png': 'dishes/dish-7.png',
    'news/Снимок_экрана_2026-05-29_162929.png': 'news/news-1.png',
}


class Command(BaseCommand):
    help = 'Синхронизирует пути изображений в базе с переименованными файлами'

    def handle(self, *args, **options):
        updated = 0

        for dish in Dish.objects.exclude(image=''):
            current = dish.image.name
            if current in IMAGE_PATHS:
                dish.image = IMAGE_PATHS[current]
                dish.save(update_fields=['image'])
                updated += 1

        for item in News.objects.exclude(image=''):
            current = item.image.name
            if current in IMAGE_PATHS:
                item.image = IMAGE_PATHS[current]
                item.save(update_fields=['image'])
                updated += 1

        self.stdout.write(self.style.SUCCESS(f'Обновлено записей: {updated}'))
