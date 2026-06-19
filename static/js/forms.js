/* Клиентская валидация форм бронирования и обратной связи. */
(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        // Минимальная дата для поля даты — сегодня.
        const today = new Date().toISOString().split('T')[0];
        document.querySelectorAll('input[type="date"]').forEach(function (input) {
            if (!input.min) {
                input.min = today;
            }
        });

        const forms = document.querySelectorAll('.js-validated-form');
        forms.forEach(function (form) {
            form.addEventListener('submit', function (event) {
                let valid = true;

                form.querySelectorAll('input, textarea, select').forEach(function (field) {
                    field.classList.remove('is-invalid');

                    if (field.hasAttribute('required') && !field.value.trim()) {
                        field.classList.add('is-invalid');
                        valid = false;
                    }

                    if (field.type === 'email' && field.value) {
                        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                        if (!re.test(field.value)) {
                            field.classList.add('is-invalid');
                            valid = false;
                        }
                    }

                    if (field.type === 'date' && field.value && field.value < today) {
                        field.classList.add('is-invalid');
                        valid = false;
                    }
                });

                if (!valid) {
                    event.preventDefault();
                    event.stopPropagation();
                }
            });
        });
    });
})();
