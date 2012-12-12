Django Assetfiles
=================

Django Assetfiles is a drop-in replacement for staticfiles which handles asset processing.


Installation
------------

1. Install package from PyPi:

    ``` sh
    $ pip install django-assetfiles
    ```

2. Replace `'django.contrib.staticfiles'` in `INSTALLED_APPS` with `'assetfiles'`:

    ``` python
    INSTALLED_APPS = (
        # ...
        # 'django.contrib.staticfiles',
        'assetfiles',
    )
    ```

3. That's it! Assetfiles will default to your [Staticfiles settings](https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/).


Usage
-----

1. Add an asset file that should be processed:

     ``` scss
     // static/css/main.scss
     $color: red;

     body {
       color: $color;
     }
     ```

2. Add a link to the processed CSS file in your template (you can use standard Staticfiles conventions):

    ``` html+django
    {% load staticfiles %}
    <link href="{% static 'css/main.css' %}" rel="stylesheet">
    ```

    Assetfiles will automatically serve up the processed version of `main.scss` at the static url of `/static/css/main.css`.

4. To serve assets in development, either use `runserver` as normal or add the following to your `urls.py`:

    ``` python
    from assetfiles.urls import assetfiles_urlpatterns

    # ... the rest of your URLconf goes here ...

    urlpatterns += assetfiles_urlpatterns()
    ```

5. For deployment, run `collectstatic` as usual and Assetfiles will process and copy over the assets:

    ``` sh
    $ python manage.py collectstatic
    $ cat public/css/main.css
    body {
      color: red; }
    ```


Copyright
---------

Copyright (c) 2012 [LocalMed, Inc.](http://localmed.com). See LICENSE for details.
