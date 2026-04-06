from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver

from django.conf import settings
from .models import CustomUser


from django.contrib.auth.models import Permission,Group
from products.models import Product,Category

@receiver(post_save, sender=CustomUser)
def send_greetings(sender, instance, created, **kwargs):
    if not created :
        return
    if instance.role == 'vendor':
        group = Group.objects.get(name='Vendor')
        subject = "Welcome vendor"
        message = "Thank you for registering!"
    else:
        group = Group.objects.get(name='Customer')
        subject = "Welcome"
        message = "Thank you for being customer!!"
    recipient = instance.email

    instance.groups.add(group)

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [recipient],
        fail_silently=False
    )

@receiver(post_migrate)
def create_groups(sender, **kwargs):
    if sender.name != 'products':
        return

    vendor_group, _ = Group.objects.get_or_create(name='Vendor')
    customer_group, _ = Group.objects.get_or_create(name='Customer')

    category_ct = ContentType.objects.get_for_model(Category)
    product_ct = ContentType.objects.get_for_model(Product)

    vendor_group.permissions.set([
        Permission.objects.get(codename='add_product', content_type=product_ct),
        Permission.objects.get(codename='change_product', content_type=product_ct),
        Permission.objects.get(codename='delete_product', content_type=product_ct),
        Permission.objects.get(codename='view_product', content_type=product_ct),

        Permission.objects.get(codename='add_category', content_type=category_ct),
        Permission.objects.get(codename='change_category', content_type=category_ct),
        Permission.objects.get(codename='delete_category', content_type=category_ct),
        Permission.objects.get(codename='view_category', content_type=category_ct),
    ])

    customer_group.permissions.set([
        Permission.objects.get(codename='view_category', content_type=category_ct),
        Permission.objects.get(codename='view_product', content_type=product_ct),
        Permission.objects.get(codename='add_to_cart', content_type=product_ct),
        Permission.objects.get(codename='view_cart', content_type=product_ct),
        Permission.objects.get(codename='delete_cart', content_type=product_ct),
        Permission.objects.get(codename='checkout', content_type=product_ct),
    ])
