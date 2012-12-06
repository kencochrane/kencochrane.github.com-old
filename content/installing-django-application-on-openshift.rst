
:date: 2012-01-14 14:05:52
:tags: django,djangocms,openshift,python,hosting,paas
:category: blog
:slug: installing-django-application-on-openshift
:author: Ken Cochrane
:title: Installing a Django application on Red Hat's OpenShift PAAS


It seems like everyone has their own `PAAS <http://en.wikipedia.org/wiki/Platform_as_a_service>`_ solution these days, and if they don't have one yet, it is just a matter of time before they will. Red Hat has recently joined in on the fun with their `OpenShift <https://openshift.redhat.com>`_ platform. 

I decided to take it for a test drive, and share my results with you. This service is still in beta and things are changing all of the time, so these notes might not work in the future, take that into consideration when using it as a guide. 

There really isn't much python documentation for this platform, and what documentation there is, is either a little out of date, or missing some important steps. Hopefully this guide will help you get your application up and running.

OpenShift is divided into two parts, Flex and Express. 

`Flex <https://openshift.redhat.com/app/flex>`_:
************************************************

    "Dedicated cloud solution.
    Get more control over your apps, or move your existing applications to the cloud with ease! Flex is a dedicated cloud solution that provides everything you need to easily scale, provision, deploy, and monitor your applications." 

Flex runs on top of your amazon EC2 account, and currently only supports Java and PHP. It is targeting the enterprise crowd and has more features compared to Express.

`Express <https://openshift.redhat.com/app/express>`_:
****************************************************** 

    "Shared cloud solution. Express is a free, cloud-based application platform for Java, Perl, PHP, Python, and Ruby applications. It's super-simple—your development environment is also your deployment environment: git push, and you're in the cloud!"

Express runs on Red Hat's servers, and currently supports Java, Ruby, PHP, Perl and Python apps. It doesn't have the same features of Flex, but if you don't need those advanced features, then express might be fine for you. Since I'm interested in deploying python apps, and Express is the only one that supports python apps, that is the one I'll show you today.

To make things easier to show you how things work, I'll create a simple django application and walk you through the steps to deploying it. I'm going to deploy a djangoCMS to express that will connect to a mysql database.

Steps:
======

1. Create an account
---------------------
Create an account by filling out the form at http://openshift.redhat.com/ and don't forget your username and password, you will need that later.

2. Install Perquisites:
-----------------------

    - `git <http://git-scm.com/>`_
    - `python <http://python.org>`_
    - openshift client
    

    **Git:**
    
    I'm not going to go over the steps to install git, for more info, you can get it from the git website. http://git-scm.com/download
    
    **Python:**
    
    If you are using a Mac or linux, it most likely already has python installed, if you are using windows, you you don't have python installed. Goto the python website and you will find instructions on how to install python on your system. http://python.org/download/
    
    **OpenShift client:**
    
    For instructions on how to Install the client go to this page.  https://openshift.redhat.com/app/express#mac Here are my steps for Mac OSX
    
.. code-block:: bash
    
            $ sudo gem install json_pure
            $ sudo gem install rhc


3. Create a domain. 
-------------------

Now that you have everything installed, your first step is to create a domain. Run the following command and  replace $mydoman and $loginemail with your own domain and the login email you used when creating an account. 

.. code-block:: bash
    
    $ rhc-create-domain -n $mydomain -l $loginemail


4. Create an application
------------------------

Now that you have a domain, you need to create an application that you can deploy to that domain. Running the following command will create a new wsgi application called 'blog'. You can name your application anything you want, within reason. We pick wsgi, because our python application will be wsgi compatible.

.. code-block:: bash

    $ rhc-create-app -a blog -t wsgi-3.2


5. Add mysql to your app
-------------------------

We want to use mysql as our database backend for this blog, so we need to add mysql to our application using the command below.

.. code-block:: bash

    $ rhc-ctl-app -a blog -e add-mysql-5.1

   
6. Add phpmyadmin to help you manage your database
---------------------------------------------------

OpenShift doesn't give you direct access to your database, so you will need a way to manage your database a different way. They provide the ability to add PHPMyAdmin to your app so that you can get to your data. This step is optional, but recommended. 

.. code-block:: bash

    $ rhc-ctl-app -a blog -e add-phpmyadmin-3.4


7. Add this upstream repo from github
-------------------------------------

When you create your application, it will create a directory with a bunch of other files and directories in it. If you were starting from scratch and building up your application you would start from here. To make things easier I created a project on github that will allow you to get up and running with DjangoCMS much faster. In order to use my project you will need to run the following commands so that it will pull down the code into your project.

.. code-block:: bash

    $ cd blog
    $ git remote add upstream -m master git://github.com/kencochrane/django-cms-openshift.git
    $ git pull -s recursive -X theirs upstream master

Once the code is downloaded, you can take a look at the code, change anything you want and when you are ready you can deploy the app.

8. Deploying the app
---------------------

To deploy all you need to do is push the repo upstream into open shift. To this, you just need to run the following command.

.. code-block:: bash

    $ git push

When it pushes you application into open shift it will do the following. (without jenkins add-on installed)

    1. stop app
    2. \*pre_build
    3. \*build
    4. start_dbs
    5. \*deploy
    6. start_app
    7. \*post_deploy

The steps marked with a * are scripts that are located in *.openshift/action_hooks/<script_name>* if you have something in those files it will run them, and if not, it will pass right by. These are very helpful if you want something to happen at points of the deployment process. For example, in the deploy script you will notice that I have some code to kick off the django syncdb, migrate, and collect static commands. These will run every time I deploy the app. 

I have also created a django management command that will check to see if there is a django admin account created and if not, it will create one and set the default password. I had to do this because there is currently no way that I know of where you can kick off django management commands after the deployment is finished. It will only create the admin account once, and every other time it will just get ignored. 

**IMPORTANT:** It is important to note that if you want to do anything related to the database, you can't do it in the *pre_build* or *build* scripts, because the database isn't available yet. This one thing caused me lots of pain, because I couldn't figure out by my migrations were not working. If you do make the mistake of trying to do something database related in the *build* script you will see an error like this. 

    "remote: ERROR 2003 (HY000): Can't connect to MySQL server on 'xxx.x.xx.x' (111)"



That's it, you can now checkout your application at (default admin account is admin/<password given at deploy time>):

    http://blog-$yourdomain.rhcloud.com


Once you visit the page you should see the djangoCMS default page. First things first, login to the django admin, and change the password from the default password to something secure. Then get started building your own app.


Helpful tips:
=============

Viewing logs:
-------------
If you would like to view your logs to see what is going on with your application you just need to run this command.

.. code-block:: bash

    $ rhc-tail-files -a blog

Application information:
------------------------
If you would like more information about your application you can run this command.

.. code-block:: bash

    $ rhc-user-info

Also checkout the README file they add when you create an application, it is pretty helpful, and might answer some common questions.


Application dependencies:
-------------------------
OpenShift uses virtualenv but it doesn't use pip, it depends on the dependencies be listed in the setup.py file. During the deploy process I did notice that it installed pip, so it might be possible to add a requirements.txt file, and then in your build action_hook script call pip install -r <path>/requirements.txt but I'm not sure if this is supported, or if it will cause problems, so it might be best to stick with what they have for now.

Static media:
-------------
If you look in wsgi/static/.htaccess there a rewrite rule to get the media to work correctly, you can use this trick for other apache tricks if you want. For more information on this checkout the README file.

What is it open shift running:
------------------------------
Red Hat linux with Apache / mod_wsgi, and mysql 5.1

What type of apps do they support?
----------------------------------
Here is the current link which can be found if you run this commands and look at the types.

.. code-block:: bash

    $ rhc-create-app -h
    
    raw-0.1, php-5.3, jbossas-7.0, rack-1.1, jenkins-1.4, perl-5.10, wsgi-3.2

What else does it support?
--------------------------
Things are changing all of the time, but if you run this command you will get a list of the current supported addons. 

.. code-block:: bash

    $ rhc-ctl-app -L

    List of supported embedded cartridges:
    
    Obtaining list of cartridges (please excuse the delay)...
    
        - metrics-0.1
        - mysql-5.1
        - jenkins-client-1.4
        - 10gen-mms-agent-0.1
        - phpmyadmin-3.4
        - rockmongo-1.1
        - mongodb-2.0

Web based control panel:
------------------------
They offer a web based control panel to do some of the things you can do with the command line, which will be nice, but it doesn't work right now. It doesn't display the correct information, and it doesn't even show the applications I have created, so I don't trust it. Hopefully these issues will get fixed in the future, and this tool will make it easier for less technical people to get started.

Conclusion:
-----------
It is nice to see another platform on the market, it is still pretty rough, and there isn't much documentation, but I found it usable. I'm sure once they stabilize things, they will spend more time on the documentation side of things. 

Other Helpful OpenShift links:
------------------------------
- `My GitHub repo for this article <https://github.com/kencochrane/django-cms-openshift>`_
- https://github.com/openshift/django-example
- http://blog.ianweller.org/2011/05/12/openshift-express-first-thoughts/

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

Update
------
2/16/2012: Full disclosure. On Feb 16th 2012, I accepted a job with dotCloud a competitor to openShift. I plan on keeping this blog post up to date and impartial. If you think there are any errors, please let me know in the comments. 

