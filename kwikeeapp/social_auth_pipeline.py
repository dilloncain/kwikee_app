from kwikeeapp.models import Customer, Driver

def create_user_by_type(backend, user, request, response, *args, **kwargs):             # Make sure to put all types
    if backend.name == 'facebook':          # if backend then.....
        avatar = 'https://graph.facebook.com/%s/picture?type=large' % response['id']        # It will create avatar from link

    if request['user_type'] == "driver" and not Driver.objects.filter(user_id=user.id):     # Checks if driver and if driver already exits
        Driver.objects.create(user_id=user.id, avatar = avatar)                             # If not, then new driver will be created
    elif not Customer.objects.filter(user_id=user.id):
        Customer.objects.create(user_id=user.id, avatar = avatar)
