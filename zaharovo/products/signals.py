from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from transliterate import translit

from .models import Category


@receiver(pre_save, sender=Category)
def create_slug_for_category(sender, instance, **kwargs):
    if not instance.slug or instance.name != instance.__class__.objects.get(
            id=instance.id).name:
        slug_base = translit(instance.name, 'ru', reversed=True)
        instance.slug = slugify(slug_base, allow_unicode=False)
