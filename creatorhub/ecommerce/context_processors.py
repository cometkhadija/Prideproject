from .models import Profile

def shop_names_processor(request):
    shop_names = Profile.objects.filter(
        role='seller',
        shop_name__isnull=False
    ).exclude(shop_name='')
    return {'shop_names': shop_names}
