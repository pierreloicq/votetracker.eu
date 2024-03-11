# run this and then populate_vote_and_position_tables.py

import json, os
from django.core.wsgi import get_wsgi_application
from decouple import config

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yvm_site.settings")
application = get_wsgi_application()

from django.contrib.auth.models import User, Group, Permission
from yvm.models import Mep#, MepUser

#### delete content
Mep.objects.all().delete()
Group.objects.all().delete()

superuser = User.objects.get(is_superuser=True)
User.objects.exclude(pk=superuser.pk).delete()

mepGroup, created = Group.objects.get_or_create(name="mepGroup")

permissions = Permission.objects.filter(codename__in=['view_position', 'change_position', 
                                                      'view_vote', 'change_vote', 'view_mep', 'change_mep'])
mepGroup.permissions.set(permissions)
mepGroup.save()

file_path = "parltrack_data/ep_meps.json"
current_term = 9

mode = 'less_secure' # less_secure | more_secure
counter = 0
with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        if '"active": true' in line:
            counter += 1
            if counter % 50 == 0:
                print(counter)
            oneline = json.loads(line[1:])

            eu_group_short = [dico['groupid'] for dico in oneline['Groups'] if '9999-12-31' in dico['end']]
            eu_group_long =  [dico['Organization'] for dico in oneline['Groups'] if '9999-12-31' in dico['end']]
            if 'Constituencies' in oneline:
                national_party = [dico['party'] for dico in oneline['Constituencies'] if dico['term'] == current_term][0]
                country = [dico['country'] for dico in oneline['Constituencies'] if dico['term'] == current_term][0]
            else:
                national_party, country = None, None
            
            mail = oneline['Mail'][0] if 'Mail' in oneline else None

            user = User.objects.create_user(username=mail, email=mail, is_staff=True,
                                            password=config('MEP_INITIAL_PASSWORD'),
                                            first_name=oneline['Name']['sur'], 
                                            last_name=oneline['Name']['family'],
                                            )
            if mode == 'more_secure':
                # password reset works only if user already has a password
                # these passwords are never disclosed to anyone. MEP's have to reset their password directly
                password = User.objects.make_random_password()
                user.set_password(password)
                user.save()
            
            mep = Mep(
                user = user,
                mep_id = oneline['UserID'],
                fullname = oneline['Name']['full'],
                gender = oneline.get('Gender'),
                birth_date = oneline.get('Birth', {}).get('date')[:10] if 'Birth' in oneline else None,
                eu_group_short = eu_group_short[0],
                eu_group_long = eu_group_long[0],
                national_party = national_party,
                country = country,
                email = mail,
                twitter = oneline['Twitter'][0] if 'Twitter' in oneline else None,
                facebook = oneline['Facebook'][0] if 'Facebook' in oneline else None,
                website = oneline['Homepage'][0] if 'Homepage' in oneline else None,
                eu_page_url = oneline.get('meta', {}).get('url'),
                photo_url = oneline.get('Photo'),
            )
            mep.save()
            mepGroup.user_set.add(user)
    


