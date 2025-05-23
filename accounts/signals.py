from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save
from .models import User,UserProfile

@receiver(post_save,sender=User)
def post_save_create_profile_receiver(sender,instance,created,**kwargs):
    # print(created)
    if created:
        UserProfile.objects.create(user=instance)
        # print("Created user profile")
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except Exception:
        #  create the user profile if not exist
            UserProfile.objects.create(user=instance)
            # print("Profile was not exists but I created one")
        # print("User is Updated")

@receiver(pre_save,sender=User)
def pre_save_profile_receiver(sender,instance,**kwargs):
    # print(instance.username,' this user is being created')
    pass