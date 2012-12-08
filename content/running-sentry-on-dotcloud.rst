
:date: 2012-01-28 23:00:33
:tags: dotcloud,django,sentry,python
:category: blog
:slug: running-sentry-on-dotcloud
:author: Ken Cochrane
:title: Running sentry on DotCloud

`Sentry <https://github.com/dcramer/sentry>`_ is a realtime event logging and aggregation platform. At it’s core it specializes in monitoring errors and extracting all the information needed to do a proper post-mortum without any of the hassle of the standard user feedback loop.

The main feature of sentry and the ability to send all of your application logs to one place, and then aggregate them, so that you only get one error email for the same error. This will keep your mailbox from flooding, when something goes wrong. 

Putting your logging server on a different server or network then your production servers is a good idea. If something goes wrong, and you can't access your servers, you can still see what errors were getting thrown before the servers started having problems. 


Follow these easy steps to get sentry up and running on DotCloud.

1. Create a place to store your project

.. code-block:: bash

    $ mkdir -p ~/projects

2. Go into the projects directory

.. code-block:: bash

    $ cd ~/projects

3. Clone git repo from github, requires git client

.. code-block:: bash

    $ git clone git://github.com/kencochrane/sentry-on-dotcloud.git
    
4. Go into the new project directory

.. code-block:: bash
    
    $ cd sentry-on-dotcloud

5. Creating the virtualenv (using virtualenvwrapper, virtualenv, and pip)

.. code-block:: bash

    $ mkvirtualenv --no-site-packages --distribute sentry-on-dotcloud

6. Install all of the Sentry requirements via pip and the requirements.txt file.

.. code-block:: bash

    $ pip install -r requirements.txt

7. Installing the dotCloud client  http://docs.dotcloud.com/firststeps/install/ (here are the steps for Linux and Mac OSX)

.. code-block:: bash

    $ sudo pip install -U dotcloud

8. Sign up for a dotcloud account https://www.dotcloud.com/accounts/register/ if you haven't already.

9. The first time you use the dotCloud account you will need to add your api key. So type dotcloud and follow the steps. You can find your API key at http://www.dotcloud.com/account/settings

.. code-block:: bash

    $ dotcloud

10. Create your dotcloud application

.. code-block:: bash

    $ dotcloud create sentry
    
11. Change the SENTRY_KEY settings in these files, to the same unique value.

    - sentry_conf.py
    - sentryproj/settings.py

Here is an example on how to generate a good unique key that you can use in the files above.

.. code-block:: python

    >>> import base64
    >>> import os
    >>> KEY_LENGTH = 40
    >>> base64.b64encode(os.urandom(KEY_LENGTH))
    '6+tSEh1qYwDuTaaQRcxUjMDkvlj4z9BU/caCFV5QKtvnH7ZF3i0knA=='

12. Add your email address to SENTRY_ADMINS in sentryproj/settings.py . This will send you emails when an error occurs.

.. code-block:: python

     SENTRY_ADMINS = ('youremail@example.com',)

13. Push your code into dotcloud

.. code-block:: bash

     $ dotcloud push sentry .

14. Find out your application url

.. code-block:: bash

     $ dotcloud url sentry

15. Open url in your browser and start using sentry on dotcloud.

16. First things first you should change the admin password from the default one that was created on deployment. The default username and password are found in the mkadmin.py file.

17. Test out sentry using the raven client to make sure it is working as it should. Open up a python shell on your local machine and do the following. 

Replace the server_url with your sentry url you found out in step 14. Make sure it ends in /store/ . Also make sure you replace my_key with your sentry key

.. code-block:: python

    >>> from raven import Client
    >>> server_url = "http://sentry-username.dotcloud.com/store/"
    >>> my_key='1234-CHANGEME-WITH-YOUR-OWN-KEY-567890'
    >>> client = Client(servers=[server_url], key=my_key)
    >>> client.create_from_text('My event just happened!')
    ('48ba88039e0f425399118f82173682dd', '3313fc5636650cccaee55dfc2f2ee7dd')

If you go to the sentry webpage you should see your test message. If not, double check everything, and see if there was any errors during the send.

Once this is all up and running you can install the raven client in your applications, and start sending your logs to sentry.

18. Optional: If you don't like the URL they gave you, you can use your custom domain. Assuming your application was sentry.www and your domain was www.example.com you would do the following

.. code-block:: bash

     $ dotcloud alias add sentry.www www.example.com

Once you get comfortable with how things work, don't forget to change your DEBUG setting to False. Go ahead and fork my project and get started today.

For more info about dotcloud, sentry, and Raven and what you can do with with it. Check out their docs
 - Sentry on DotCloud GitHub repo : https://github.com/kencochrane/sentry-on-dotcloud
 - DotCloud overview: http://docs.dotcloud.com/firststeps/platform-overview/
 - Sentry Documentation: http://sentry.readthedocs.org/en/latest/index.html
 - Raven Documentation: http://raven.readthedocs.org/en/latest/index.html
 
Links:
 - Virtualenv : http://pypi.python.org/pypi/virtualenv
 - pip : http://www.pip-installer.org/
 - virtualenvwrapper : http://www.doughellmann.com/projects/virtualenvwrapper/
 - git : http://git-scm.com/

