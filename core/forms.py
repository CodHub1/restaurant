"""Формы пользовательских данных."""
from django import forms
from django.utils import timezone

from .models import Booking, Feedback


class BookingForm(forms.ModelForm):
    """Форма бронирования столика."""

    class Meta:
        model = Booking
        fields = ('name', 'phone', 'date', 'time', 'guests', 'note')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя',
                'required': True,
                'minlength': 2,
                'maxlength': 100,
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (___) ___-__-__',
                'required': True,
                'pattern': r'[\d\+\-\(\)\s]{7,20}',
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True,
            }),
            'time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'required': True,
            }),
            'guests': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 20,
                'required': True,
            }),
            'note': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Особые пожелания (необязательно)',
            }),
        }

    def clean_guests(self):
        guests = self.cleaned_data.get('guests')
        if guests is None or guests < 1:
            raise forms.ValidationError('Количество гостей должно быть не меньше 1.')
        if guests > 20:
            raise forms.ValidationError('Для брони больше 20 человек свяжитесь с нами по телефону.')
        return guests

    def clean(self):
        cleaned = super().clean()
        date = cleaned.get('date')
        time = cleaned.get('time')

        if date and time:
            booking_dt = timezone.make_aware(
                timezone.datetime.combine(date, time)
            )
            if booking_dt < timezone.now():
                raise forms.ValidationError(
                    'Нельзя забронировать столик на прошедшую дату или время.'
                )

            exists = Booking.objects.filter(date=date, time=time).exclude(
                status=Booking.STATUS_CANCELLED
            ).exists()
            if exists:
                raise forms.ValidationError(
                    'На указанные дату и время уже есть бронь. '
                    'Пожалуйста, выберите другое время.'
                )

        return cleaned


class FeedbackForm(forms.ModelForm):
    """Форма обратной связи."""

    class Meta:
        model = Feedback
        fields = ('name', 'email', 'message')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя',
                'required': True,
                'minlength': 2,
                'maxlength': 100,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com',
                'required': True,
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Ваше сообщение',
                'required': True,
                'minlength': 5,
            }),
        }
