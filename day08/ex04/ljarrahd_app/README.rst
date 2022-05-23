=====
ljarrahd
=====

ljarrahd is a Django app to upload images.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "ljarrahd" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'ljarrahd',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('ljarrahd/', include('ljarrahd.urls')),

3. Run ``python manage.py migrate`` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a ljarrahd (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/ljarrahd/ to participate in the ljarrahd.