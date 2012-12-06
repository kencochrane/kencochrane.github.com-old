
:date: 2011-04-14 10:55:09
:tags: percona,mysql,upgrade,centos5,rhel5,linux
:category: blog
:slug: upgrading-mysql-50x-percona-mysql-51x-rhel5-or-cen
:author: Ken Cochrane
:title: Upgrading MySQL 5.0.x to Percona MySQL 5.1.x RHEL5 or CENTOS 5

Upgrade the stock MySQL 5.0.x build to the new stable MySQL 5.1.x Percona version.  Here are my notes on upgrading on Red Hat Enterprise Linux 5 (RHEL5) or CentOS5.

First we need to stop mysql

.. code-block:: bash

    service mysql stop;
   
I'm assuming that you don't have the percona repo installed on your machine, if not follow this link on how to set it up. `Setting up Percona RPM Repo <http://www.percona.com/docs/wiki/percona-server:release:start>`_

.. code-block:: bash

    mkdir -p /tmp/downloads
    cd /tmp/downloads
    wget http://www.percona.com/redir/downloads/percona-release/percona-release-0.0-1.i386.rpm
    sudo rpm -Uhv percona-release-0.0-1.i386.rpm    

   
Now we need to remove the old MySQL 5.0 binaries. (Don't worry this will leave your data.)
   
.. code-block:: bash

    yum remove -y mysql-server mysql mysql-devel mysql-test mysql-bench
   
Now install the new Percona MySQL 5.1.x binaries. (depending on your connection this might take a few minutes)
   
.. code-block:: bash

    yum install -y Percona-Server-devel-51 Percona-Server-shared-51 Percona-Server-test-51 Percona-Server-client-51 Percona-Server-server-51
   
During the install it will throw out some warnings, make sure you write those down, and make the changes that it recommends. Here are a few of mine.

.. code-block:: bash

    110208 16:44:52 [Warning] '--log_slow_queries' is deprecated and will be removed in a future release. Please use ''--slow_query_log'/'--slow_query_log_file'' instead.
    110208 16:44:52 [Warning] '--log' is deprecated and will be removed in a future release. Please use ''--general_log'/'--general_log_file'' instead.

Assuming the install went well, now we need to upgrade the data to the new format. (replace <mysql admin user> with your mysql admin username, and enter password when prompted)

.. code-block:: bash

    mysql_upgrade -u <mysql admin username> -p

Now if your upgrade was anything like mine it had a bunch of errors like this.

.. code-block:: bash

    db_name.table_name
    error    : Table upgrade required. Please do "REPAIR TABLE table_name" or dump/reload to fix it!
       
When you try to repair the table you get this.

.. code-block:: bash

    db_name.table_name
    note     : The storage engine for the table doesn't support repair
       
Thanks to Peter Zaitsev `mysql_upgrade and Innodb Tables <http://www.mysqlperformanceblog.com/2010/05/14/mysql_upgrade-and-innodb-tables/>`_ we know that we can do the following to fix it.
   
.. code-block:: sql

    ALTER TABLE db_name.table_name ENGINE=INNODB;
   
We just need to run this command for each table that threw an error and it should fix it. (If you have lots of data this might take a while, I had some tables that took over 2 hours)

Once you think that you have all of the tables fixed, you can run this command and it will check all of your tables and let you know if you are good or not. If you still have errors, repeat the steps above until all tables pass.

.. code-block:: bash

    mysqlcheck -A --check-upgrade
   
Hopefully everything passed for you, and you now have a fully upgraded database. It is important to note that there is another option besides running the table alter. You could have dumped all of the data prior to the upgraded and then restored it once the database was upgraded. This process would most likely take a lot longer.


