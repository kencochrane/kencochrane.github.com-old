
:date: 2011-06-27 06:48:18
:tags: django,python,deployment,gunicorn,supervisord,fabric,centos5,nginx,linux
:category: blog
:slug: django-gunicorn-nginx-supervisord-fabric-centos55
:author: Ken Cochrane
:title: Setting up Django with Green Unicorn, nginx, supervisord and fabric on CentOS 5.5

When I first started working with django I deployed my apps using apache and mod_python. Then after a little while I started playing with nginx and switched my setup so that nginx was serving the static content and reverse proxied requests back to apache and mod_python. Not too long after that, I switched out mod_python with mod_wsgi and ran mod_wsgi in daemon mode. 

This setup worked well for a while, but one thing I never really liked was the fact that I needed to run apache which is pretty heavy even when you strip out all the unused modules. Apache is great, but all I was really using it for was a router between nginx and mod_wsgi, I wasn't using any of the other features in apache. 

I looked at fastcgi and uswgi and they looked good, but for one reason or another I never made the jump. Recently I have been hearing a lot of good things about green unicorn, so I decided to check it out. When I first looked at it, it was fairly new and because of this a little concerned with stability, so I kept and eye on it and watched it mature. 

While I was waiting for green unicorn to mature I ended up doing a lot of research on the `new python hosting services <http://kencochrane.net/blog/2011/06/django-hosting-roundup-who-wins/>`_ that recently hit the market. Three out of the five services that I looked were using green unicorn, the other two were using uWSGI. 

The fact that these three services are basing there new businesses on green unicorn gave it a lot of credibility. Not too long after that I started playing with green unicorn to see what it would take to get my sites up and running. 

The first thing that I noticed was that I didn't need to create a wsgi file if I used their gunicorn_django command, which was pretty sweet. The fact that they built it into the service shows you that django is a first class citizen. 

The second thing that I noticed was that I needed a way to start up green unicorn and keep it running, something that apache does for you with mod_wsgi. I did a little bit of research and found out that supervisord would work perfectly for what I needed to do with green unicorn.

Because seeing is better then reading, I'll guide you throw the steps that you will need to do in order to get your system setup in a way that will make using green unicorn very easy, especially if you want to run more then one website on your server. I'm going to use a 256MB rackspace cloud instance running centos 5.5. 

Create a rackspace cloud server
-------------------------------
Go into the rackspace cloud server management website and allocate yourself a new 256MB CentOS 5.5 server or if you prefer do the same thing using their API. Now that you have a server and the root password, follow along step by step to get you system all setup.

Software and versions
---------------------

* RackSpace Cloud Server 256MB 
* CentOS 5.5
* Python 2.6.6
* nginx 1.0.4
* supervisord 3.0a10
* virtualenv 1.6.1
* pip 1.0.1
* gunicorn 0.12.2
* fabric 1.1.0


Bitbucket project
-----------------
To make things easier I have created a django bootstrap project directory with all of the file used in the blog post. It is located here, so feel free to clone and fork.

https://bitbucket.org/kencochrane/django-gunicorn-nginx-supervisord-bootstrap/

Login to server
---------------
.. code-block:: bash

    ssh root@<RackSpaceIP>


Update packages
---------------
.. code-block:: bash

    yum -y update

Install packages
----------------
You might not need all of these right now, but I normally need these down the line, so doing them all now.

.. code-block:: bash

    yum -y install emacs readline-devel ncurses-devel libevent-devel glib2-devel libjpeg-devel freetype-devel bzip2 bzip2-devel bzip2-libs openssl-devel pcre pcre-devel gpg make gcc yum-utils unzip


Add a django user as a system user
----------------------------------
.. code-block:: bash

    useradd -d /opt/django -m -r django

Set password for django to what ever you want
---------------------------------------------
.. code-block:: bash

    passwd django

Setup directories
-----------------
.. code-block:: bash

    mkdir -p /opt/django
    mkdir -p /opt/django/apps
    mkdir -p /opt/django/logs
    mkdir -p /opt/django/logs/nginx
    mkdir -p /opt/django/logs/apps
    mkdir -p /opt/django/configs
    mkdir -p /opt/django/scripts
    mkdir -p /opt/django/htdocs
    mkdir -p /opt/django/tmp
    mkdir -p /opt/django/configs/nginx
    mkdir -p /opt/django/configs/supervisord
    mkdir -p /opt/django/apps/my_app

Add blank html page
-------------------
.. code-block:: bash

    echo "<html><body>nothing here</body></html> " > /opt/django/htdocs/index.html


Install Zlib
------------
.. code-block:: bash

    # download from zlib.net
    mkdir -p /tmp/downloads
    cd /tmp/downloads
    wget http://www.zlib.net/zlib-1.2.5.tar.gz
    tar -xvzf zlib-1.2.5.tar.gz
    cd zlib-1.2.5
    ./configure -s
    make install


Install python 2.6.6
--------------------
CentOS 5.5 doesn't come with python2.6 pre installed so we need to do that on our own.

.. code-block:: bash

    mkdir -p /tmp/downloads
    cd /tmp/downloads
    wget http://www.python.org/ftp/python/2.6.6/Python-2.6.6.tgz
    tar -xvzf Python-2.6.6.tgz
    cd Python-2.6.6
    ./configure --enable-shared
    make
    make altinstall


Add the following to /etc/profile
---------------------------------
We need to add the lib path to the LD_LIBRARY_PATH or else you will get an error saying it can't find libpython2.6.so.1.0

.. code-block:: bash

    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib/:/usr/local/lib64/

Source the new profile
----------------------
.. code-block:: bash

    source /etc/profile


Install distribute
------------------
.. code-block:: bash

    mkdir -p /tmp/downloads
    cd /tmp/downloads
    curl -O http://python-distribute.org/distribute_setup.py
    python2.6 distribute_setup.py


Install Pip & virtualenv
------------------------
.. code-block:: bash

    mkdir -p /tmp/downloads
    cd /tmp/downloads
    curl -O -k https://raw.github.com/pypa/pip/master/contrib/get-pip.py
    python2.6 get-pip.py
    pip install virtualenv


Install supervisor
------------------
.. code-block:: bash

    pip install supervisor


Install mercurial
-----------------
.. code-block:: bash

    pip install mercurial



Install NGINX
-------------
.. code-block:: bash

    mkdir -p /tmp/downloads
    cd /tmp/downloads
    wget http://nginx.org/download/nginx-1.0.4.tar.gz
    tar -xzvf nginx-1.0.4.tar.gz
    cd nginx-1.0.4
    ./configure --sbin-path=/usr/local/sbin --with-http_ssl_module --with-http_stub_status_module
    make
    /etc/init.d/nginx stop
    sleep 2
    sudo make install
    sudo chmod +x /usr/local/sbin/nginx


Install my app
==============

Add first virtualenv
--------------------
.. code-block:: bash

    cd /opt/django/apps/my_app/
    virtualenv --distribute --no-site-packages v0.1

    # make this a post_create hook?
    touch /opt/django/apps/my_app/v0.1/.venv

    cd /opt/django/apps/my_app/v0.1/
    hg clone https://bitbucket.org/kencochrane/django-gunicorn-nginx-supervisord-bootstrap my_app

    ln -s /opt/django/apps/my_app/v0.1 /opt/django/apps/my_app/current

    ln -s /opt/django/apps/my_app/current/my_app/conf/nginx.conf /opt/django/configs/nginx/myapp.conf

    ln -s /opt/django/apps/my_app/current/my_app/conf/supervisord.conf /opt/django/configs/supervisord/myapp.conf

    # activate the ve
    source /opt/django/apps/my_app/current/bin/activate
    cd /opt/django/apps/my_app/current/my_app/
    ./bootstrap.py


Configure nginx
---------------
.. code-block:: bash

    # as root
    mkdir -p /etc/nginx
    ln -s /opt/django/apps/my_app/current/my_app/server/etc/nginx.conf /etc/nginx/nginx.conf
    ln -s /usr/local/nginx/conf/mime.types /etc/nginx/mime.types
    ln -s /opt/django/apps/my_app/current/my_app/server/init.d/nginx /etc/init.d/nginx
    chmod 755 /etc/init.d/nginx 
    chkconfig --add nginx
    chkconfig nginx on

Configure Supervisord
---------------------
.. code-block:: bash

    # as root
    ln -s /opt/django/apps/my_app/current/my_app/server/etc/supervisord.conf  /etc/supervisord.conf
    ln -s /opt/django/apps/my_app/current/my_app/server/init.d/supervisord /etc/init.d/supervisord
    chmod 755 /etc/init.d/supervisord
    chkconfig --add supervisord
    chkconfig supervisord on


Firewall
--------
We need to open up the firewall so that we are allowed connection, if you don't know anything about this, check out these links.

http://cloudservers.rackspacecloud.com/index.php/Firewalls
http://cloudservers.rackspacecloud.com/index.php/Introduction_to_iptables
http://cloudservers.rackspacecloud.com/index.php/Sample_iptables_ruleset

.. code-block:: bash

    # Open http port 80
    iptables -I RH-Firewall-1-INPUT -p tcp --dport 80 -j ACCEPT


.bashrc file changes
--------------------
I can't remember where I saw this little trick, if you know please let me know so that I can give them credit. If you put a file in your mercurial directory called .venv, when you cd into the directory this little bash hack will automatically activate your virtual environment for you. This allows you to have something similar to virtualenvwrapper in this custom setup.

Add this code to the .bashrc file

.. code-block:: bash

    emacs /opt/django/.bashrc
    #
    # User specific aliases and functions
    has_virtualenv() {
        if [ -e .venv ]; then
            deactivate >/dev/null 2>&1
            source bin/activate
        fi
    }

    venv_cd () {
        cd "$@" && has_virtualenv
    }

    alias cd="venv_cd"

    #end of changes
    
    # source the file to get new changes in active shell
    source /opt/django/.bashrc

Change permissions of the django home directory to django
---------------------------------------------------------
This cleans up and left over root ownership

.. code-block:: bash

    chown -R django:django /opt/django/*

Switch to django user
---------------------
.. code-block:: bash

    su - django

Start up nginx
--------------
.. code-block:: bash

    service nginx start

Startup supervisord
-------------------
.. code-block:: bash

    service supervisord start

Test Nginx and supervisord
--------------------------
Check supervisord status

.. code-block:: bash
    
    supervisorctl status
    my_app                           RUNNING    pid 13594, uptime 0:00:05

To check nginx go to the IP or domain name for your rackspace server in your browser and make sure it worked.

Updating the application using fabric
-------------------------------------
Inside of the bitbucket project directory there is a file called fabfile.py. This file will allow you to update the application from your machine whenever you want just by calling one command. 

It will prompt you for your hostname and password for the django user. Then it will go out to the rackspace server and pull and update the app and restart the application in supervisord. It is very basic for right now, but should get you started if you want to do more advanced stuff.

.. code-block:: bash
    
    fab update_server
    

Conclusion
----------

Now that we have everything setup, if you want to add a new application to our setup all we need to do is.

* create a new directory under apps
* create the virtualenv
* run the bootstrap to install the software
* make sure that the application has a supervisord and nginx configuration file
* symlink those files to the correct locations in the config directory
* run any python management commands you might need to run (syncdb, migrate, etc)
* reload supervisord and nginx
* you should be good to go. 

I hope this was helpful to someone besides myself, if it was helpful for you please let me know in the comments. 


