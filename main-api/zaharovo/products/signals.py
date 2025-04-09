from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.utils.text import slugify
from .models import Category


@receiver(pre_save, sender=Category)
def create_slug_for_category(sender, instance, **kwargs):
    # Если slug не задан, создаём его на основе name
    if not instance.slug:
        instance.slug = slugify(instance.name, allow_unicode=True)
    # Если объект уже сохранён, можно проверить, изменилось ли имя
    elif instance.pk:
        try:
            old_instance = instance.__class__.objects.get(pk=instance.pk)
            if old_instance.name != instance.name:
                instance.slug = slugify(instance.name, allow_unicode=True)
        except instance.__class__.DoesNotExist:
            # Если объект не найден, ничего не делаем
            pass
