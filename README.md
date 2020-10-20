# coliving

# Setup Locally
Create a virtualenv
activate virtualenv

pip install -r requirements.txt

rename the .env.sample to .env and fill the creadentials

// do the following on shell

from memberships.models import Membership
Membership.objects.create(slug="free",membership_type="Free",price=0,stripe_plan_id="price_HKZ2whEV0LZ2vm")
Membership.objects.create(slug="lease",membership_type="Lease Holder",price=15,stripe_plan_id="price_HKXVQp5Ll4tcyR")
Membership.objects.create(slug="landlord",membership_type="Landlord",price=63,stripe_plan_id="price_1HEg76GfkeLvAqVOBqNticFz")
// shell code end


python manage.py runserver

# How to contribute
Make a new branch from development, add/update your code then merge it with development and push to origin. Others will test and then be merged to master and deployed. 
