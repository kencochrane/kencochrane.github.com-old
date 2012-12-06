
:date: 2012-01-15 13:30:13
:tags: django,djangocms,stackato,python,hosting,paas
:category: blog
:slug: getting-djangocms-up-and-running-on-stackato
:author: Ken Cochrane
:title: Getting DjangoCMS up and running on ActiveState's Stackato

ActiveState has recently started their own PAAS based on `CloudFoundry <http://cloudfoundry.org/>`_ this blog post is to help you get up and running quickly with a Django CMS installation, and hopefully give you enough information to get your own applications on there as well.

To keep things simple, I'll just go through the steps that are required in order to get this up and running and add some comments along the way. If I missed anything or if you have any questions, please ask in the comments.

-------------------
Running on Stackato
-------------------

1. Register for an account
--------------------------

Go to http://community.activestate.com/stackato and register for your account. They are currently in beta, and you need to be approved before they will give you access.

2. Install the client
---------------------

There are a few different options, follow the steps outlined here. http://docs.stackato.com/quick-start.html#stackato-client-setup

I tried the option where you download the file, and rename it and put it in your path. It wasn't complicated, but it wasn't clean either. I chose this option because I didn't want to install `pypm <http://code.activestate.com/pypm/>`_, so I'm not sure if that way is easier or not. 

3. Register your client to the cloud
------------------------------------

Now that you have the client installed you need to tell it which cloud to deploy too. With Stackato, you can run your own local cloud as well as using the sandbox that ActiveState provided. To make things simple, I'm going to use the sandbox. If you want to use the local cloud you will need to `read the directions <http://docs.stackato.com/quick-start.html#accesssing-the-micro-cloud>`_ on how to use the local cloud option.

.. code-block:: bash

    $ stackato target api.sandbox.activestate.com
    > Successfully targeted to [https://api.sandbox.activestate.com]
    
4. Login to stackato
--------------------

Once you point your client in the correct location, you will need to login to the cloud. You can find your login information on your `activestate account page <https://account.activestate.com/>`_. Type the following and answer the questions when prompted.

.. code-block:: bash

    $ stackato login
    > Successfully logged into [https://api.sandbox.activestate.com]
    
5. Download this github repo
----------------------------

To make things easier, I have made a simple django project that has all of the configuration information setup so that you don't need to do anything if you want to use djangoCMS. Look at my `github repo <https://github.com/kencochrane/django-cms-stackato>`_, and see how I did things if you want to get your own application up and running. If you want to use djangoCMS, then all you have to do is follow these steps.

.. code-block:: bash

    $ cd ~/projects
    $ git clone git://github.com/kencochrane/django-cms-stackato.git
    $ cd django-cms-stackato
    
6. Deploy the project to stackato
---------------------------------

Once you have your application ready, you can push the application to the cloud. When you do this it will prompt you for a bunch of questions, answer them and keep track of what you picked for a website url, because you will need that later. My application is called myblog, but you can put whatever you want, just change myblog with your name.

.. code-block:: bash

    $ stackato push myblog
    
7. Initialize the database (optional)
-------------------------------------

I have set this up so that it should happen automatically at deployment see the stackato.yml file for more details. If you want to run the commands outside of deployments this is what you can do.

.. code-block:: bash

    $ stackato run myblog python mycms/manage.py syncdb --noinput
    
8. Run south migrations (optional)
----------------------------------

I have set this up so that it should happen automatically at deployment see the stackato.yml file for more details. If you want to run the commands outside of deployments this is what you can do. It is important to note *I had to run more then once since it was killed the first time. Maybe it took too long?*.

.. code-block:: bash

    $ stackato run myblog python mycms/manage.py migrate --noinput
    
9. Collect the static files (optional)
--------------------------------------

I have set this up so that it should happen automatically at deployment see the stackato.yml file for more details. If you want to run the commands outside of deployments this is what you can do.

.. code-block:: bash

    $ stackato run myblog python mycms/manage.py collectstatic --noinput
    
10. Create the django admin account
-----------------------------------

Now that you have your application installed and you have your database setup, you need to create the django admin, you can do that with ths django management command.
Make sure you replace the variables with your values.

.. code-block:: bash

    $ stackato run myblog python mycms/manage.py createsuperuser --username=admin --email=admin@example.com --noinput
    
11. Change the password for the admin user
------------------------------------------

You need to set a password for the admin account so that you can login. Pick a more secure password then the example I have here. *(notice it is changepassword2 not changepassword)*

.. code-block:: bash

    $ stackato run myblog python mycms/manage.py changepassword2 admin secret123P@ssw0rd!

12. Open up the url in your browser
-----------------------------------

When you open up the URL that you picked when you deployed in your browser you should find the DjangoCMS pony welcome page. If not, try debugging using some of the tips below.

----------
Conclusion
----------

That is it, I did all the hard work, so you should be able to follow those simple steps and get djangoCMS up and running in no time. Once you get that working, play around with it, and let me know what you think. Have you tried the other PAAS options yet, if not check those out as well, and then let me know which ones you like better and why. I have written blog posts about most of them at this point, so feel free to check those out (links below), and have fun playing around.

Other Useful Information
------------------------

Starting an application if it isn't running
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    $ stackato start myblog
    
Restarting an application
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    $ stackato restart myblog
    
Stopping an application
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    $ stackato stop myblog

Updating application after it is already deployed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    $ stackato update myblog
    
Find out how many instances you have running
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    $  stackato stats myblog
    
Find out which apps you have installed, and their status
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    $ stackato apps

Find out what logs you have for your applications
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    $ stackato files myblog logs

Viewing logs for your app
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    $ stackato logs myblog --all
    
Running cat on a particular log file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    $ stackato run myblog cat ../logs/myapp-err.log

-----
Links
-----
- My github repo for this blog post: https://github.com/kencochrane/django-cms-stackato
- Stackato Client command reference: http://docs.stackato.com/commands.html#command-ref-client
- stackato.yml reference: http://docs.stackato.com/client.html#configure-stackato-yml
- Stackato quick start guide: http://docs.stackato.com/quick-start.html
- Stackato Sandbox Ground Rules, Content Policy and Quotas: http://docs.stackato.com/sandbox.html
- ActiveState Account page: https://account.activestate.com/
- pip : http://www.pip-installer.org/
- git : http://git-scm.com/

My other articles related to PAAS:
----------------------------------
- `My Experiences with ep.io <http://kencochrane.net/blog/2011/04/my-experiences-with-epio/>`_ 
- `AppHosted.com Django Hosting Service Review <http://kencochrane.net/blog/2011/05/apphosted-com-django-hosting-review/>`_ 
- `My Day in Gondor.io <http://kencochrane.net/blog/2011/04/my-day-gondorio/>`_
- `Deploying my Django application to DotCloud.com <http://kencochrane.net/blog/2011/04/deploying-my-django-application-to-dotcloud/>`_
- `DjangoZoom.com Review <http://DjangoZoom.com>`_
- `Django hosting roundup <http://kencochrane.net/blog/2011/06/django-hosting-roundup-who-wins/>`_
- `Installing DjangoCMS on Heroku in 13 easy steps <http://kencochrane.net/blog/2011/12/installing-djangocms-on-heroku-in-13-easy-steps/>`_
- `Installing DjangoCMS on dotCloud in 12 easy steps <http://kencochrane.net/blog/2011/12/installing-djangocms-dotcloud-12-easy-steps/>`_
- `Developers guide to Running Django Applications on Heroku <http://kencochrane.net/blog/2011/11/developers-guide-for-running-django-apps-on-heroku/>`_
- `Installing a Django application on Red Hat's OpenShift PAAS <http://kencochrane.net/blog/2012/01/installing-django-application-on-openshift/>`_

Update
------
2/16/2012: Full disclosure. On Feb 16th 2012, I accepted a job with dotCloud a competitor to Stackato. I plan on keeping this blog post up to date and impartial. If you think there are any errors, please let me know in the comments. 

