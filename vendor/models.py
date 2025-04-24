from django.db import models
from accounts.models import User,UserProfile
from accounts.utils import *
class Vendor(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
  user_profile = models.OneToOneField(UserProfile,on_delete=models.CASCADE, related_name='userprofile')
  vendor_name = models.CharField(max_length=50)
  vendor_license = models.ImageField(upload_to='vendor/liscense/')
  is_approved = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  modified_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.vendor_name
  
  def save(self,*args,**kwargs):
    if self.pk is not None:
      # update
      orig = Vendor.objects.get(pk=self.pk)
      if orig.is_approved != self.is_approved:
        # send email notification
        mail_template = "accounts/emails/admin_approval_email.html"
        context = {
               'user':self.user,
               'is_approved':self.is_approved,
            }
        if self.is_approved:
          # send approval email
            mail_subject = "Congratulations! Your Restaurant has been approved."
            send_notification(mail_subject,mail_template,context)
        else:
          # send disapproval email
            mail_subject = "Sorry! Your Restaurant has been disapproved."
            send_notification(mail_subject,mail_template,context)
      else:
        # no change in approval status
        pass
    return super(Vendor,self).save(*args,**kwargs)
  