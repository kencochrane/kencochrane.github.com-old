
:date: 2011-12-30 14:53:35
:tags: django,supervisor,gunicorn,newrelic
:category: blog
:slug: using-new-relic-with-supervisord-and-gunicorn
:author: Ken Cochrane
:title: Using New Relic with supervisord and gunicorn

New Relic recently added support for python to their awesome web application performance tool, and I have been playing with it on a number of projects. 

Installing and configuring new relic is pretty well covered in their own `documentation <http://newrelic.com/docs/python/>`_, so there is no reason for me to repeat that here. One thing that isn't covered in the documentation is how to use new relic if you are using supervisord to control your gunicorn processes, and I'll take this time right now to show you what I did.

Setting up new relic with supervisord and gunicorn is pretty easy. All that you need to do, is change your supervisor.conf file and then update your supevisor config, and you are good to go.

Here is the supervisor.conf file for my awesome app, before I installed new relic.

*Note: These are not my real conf files, they have been changed to protect the guilty, so please excuse any typos.*

.. code-block:: txt

    [program:awesome_app]
    directory=/opt/apps/awesome_home/awesome_app/
    command=/opt/apps/awesome_home/bin/python2.6 /opt/apps/awesome_home/bin/gunicorn_django -c /opt/apps/awesome_home/awesome_app/conf/gunicorn.conf
    user=aweman
    autostart=true
    autorestart=true
    environment=HOME='/opt/apps/awesome_home/awesome_app/',DJANGO_SETTINGS_MODULE='settings'

After I installed new relic. All you need to do is add the 'newrelic-admin run-program' command before the 'gunicorn_django' command and add an ENV variable called NEW_RELIC_CONFIG_FILE that is pointing to your newrelic.ini file.

.. code-block:: txt

    [program:awesome_app]
    directory=/opt/apps/awesome_home/awesome_app/
    command=/opt/apps/awesome_home/bin/newrelic-admin run-program /opt/apps/awesome_home/bin/gunicorn_django -c /opt/apps/awesome_home/awesome_app/conf/gunicorn.conf
    user=aweman
    autostart=true
    autorestart=true
    environment=HOME='/opt/apps/awesome_home/awesome_app/',DJANGO_SETTINGS_MODULE='settings',NEW_RELIC_CONFIG_FILE=/opt/apps/awesome_home/awesome_app/conf/newrelic.ini
    

Now that you have the new configuration setup, you will need to let supervisord know that you have changed t he configuration for that app. If you run the update command it will prompt supervisord to reread the configuration file for that app, and reload the config, and then restart the application with the new configuration.

.. code-block:: bash

    $ supervisorctl update


Another thing that is important to note here, is the fact that New Relic currently doesn't work well with Gunicorn in gevent mode. If you try to use gevent with gunicorn and new relic, it may not start up at all, or just not work as it should. Here is what they say in the `Known Issues <http://newrelic.com/docs/python/status-of-python-agent>`_ section of their docs.

    Gunicorn gevent mode - When using gevent mode of gunicorn and the 'newrelic-admin run-program' command is used to wrap the invocation of gunicorn, the hosted web application can fail in strange ways. One way this is manifesting is with requests blocking for a period of 1 minute.
    The cause of the problem is believed in this case to specifically relate to the order in which module imports are occuring. The monkey patching performed by gevent is not working properly for the case where the Python threading module is imported before the gevent monkey patching routine is run.


Because of this, I have changed my gunicorn's to use eventlet when using new relic, and that seems to work fine. I normally prefer to use gevent, so hopefully they will be able to fix the issue with gevent so I can revert back to that setup.

All and all I have been pretty happy with new relic, it has helped us find issues with our code that would have been a pain otherwise. There support has been awesome, and they have been adding new fixes/ improvements all the time. Can't wait to see what else they have in store for the future. I would try it out if you can, they have a lite version that is free which even includes server monitoring.


