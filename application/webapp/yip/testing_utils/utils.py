"""
Testing utilities and functions
"""


import random
import string

from django.contrib.auth.models import User

from user_profiles.models import UserProfile, YogaStyle


def email_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """
    Generate a random email
    """
    email = ''.join(random.choice(chars) for _ in range(size)) + '@gmail.com'
    return email.lower()

def password_generator(size=8, chars=string.ascii_uppercase + string.digits):
    """
    Generate a random password
    """
    return ''.join(random.choice(chars) for _ in range(size))

def create_test_user(email=None, password=None):
    """
    Create a test user
    """
    if email:
        email = email
    else:
        email = email_generator()

    if password:
        password = password
    else:
        password = password_generator()

    test_user = User.objects.create(email=email, username=email)
    test_user.set_password(password)
    test_user.save()
    return test_user

def create_test_user_profile(user=None):
    """
    Create a test user profile
    """
    if user:
        user = user
    else:
        user = create_test_user()

    test_profile = UserProfile.objects.create(
        user=user,
        first_name='Taliesin',
        last_name='Oppenheimer',
        country='USA',
        state='MA',
        city='Cambridge',
        street='2022 Massachusetts Avenue',
        postal_code='02140',
        is_teacher=False
    )
    return test_profile

def create_test_yoga_style(title=None, public=True):
    """
    Create a test yoga style
    """
    if title:
        title = title
    else:
        index = random.randint(0,4)
        styles = [
            'Iyengar',
            'Vinyasa',
            'Ashtanga',
            'Kundalini',
            'Bikram'
        ]
        yoga_style = YogaStyle.objects.create(
                title=styles[index], public=public)
        return yoga_style

def print_response_info(response, test_name=None):
    """
    Format and print test response
    """
    if test_name:
        print('TEST NAME: %s' % test_name)

    print('Response status code: \t %d' % response.status_code)
    print('Response JSON content:')
    print(response.content)
    print('\n')

