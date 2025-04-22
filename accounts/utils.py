def detectUser(user):
  if user.role == 1:
    redirectUrl = 'vendorDashboard'
    return redirectUrl
  elif user.role == 2:
    redirectUrl = 'customerDashboard'
    return redirectUrl
  elif user.is_superadmin and user.role == None:
     redirectUrl = '/admin'
     return redirectUrl