.. image:: https://readthedocs.org/projects/django-epsg-cache/badge/?version=latest
    :target: https://django-epsg-cache.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://badge.fury.io/py/django-epsg-cache.svg
    :target: https://pypi.org/project/django-epsg-cache/
    :alt: PyPi version

django-epsg-cache
=================

In geo applications `coordinate tuples <https://wiki.osgeo.org/wiki/Axis_Order_Confusion>`_ can be ordered either (x,y) or (y,x) or (x,y) but meant as (y,x). 
Based on this problem and on some geo spatial standards which requires to retreive the correct axis order from the `epsg registry <https://epsg.org/API_UsersGuide.html>`_, we developed this simple django app to cache the spatial reference objects.

Quick-Start
-----------

Install it as any other django app to your project:

.. code-block:: bash

    $ pip install django-epsg-cache

.. warning::
    As pre requirement you will need to install the `gdal and geos binaries <https://docs.djangoproject.com/en/4.2/ref/contrib/gis/install/geolibs/>`_ on your system first.
    
See the `documentation <https://django-epsg-cache.readthedocs.io/en/latest/index.html>`_ for details.
