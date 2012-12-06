
:date: 2010-05-13 20:09:33
:tags: Mercurial,RHEL5,python,linux
:category: blog
:slug: mercurial-1_5_1-on-RHEL5-using-python2_5
:author: Ken Cochrane
:title: Installing Mercurial 1.5.1 on Red Hat Enterprise Linux 5 (RHEL5) using Python 2.5


Installing Mercurial 1.5.1 on Red Hat Enterprise Linux 5 (RHEL5) using Python 2.5
---------------------------------------------------------------------------------

My RHEL5 setup uses python2.5 which I compiled from source, since RHEL5 only comes with python2.4.

Because I didn't use the built in python 2.4 version I couldn't do the simple 

.. code-block:: bash

    $ yum install mercurial

Instead I need to build mercurial from source, which isn't too bad. Just do the following.

**as Root**

.. code-block:: bash

    $ wget http://mercurial.selenic.com/release/mercurial-1.5.1.tar.gz
    $ tar -xvzf mercurial-1.5.1.tar.gz
    $ cd mercurial-1.5.1 
    $ make PYTHON=python2.5 install

If you get the following error:

.. code-block:: bash

    $ python2.5 setup.py build
    $ Couldn't import standard bz2 (incomplete Python install).
         make:  [build] Error 1


Then when you installed python 2.5 you didn't have the bzip2 libs installed so it didn't include them in the python2.5 install. No big deal all you need to do is install those libs and then recomplile python 2.5

**install bzip2 libs**

.. code-block:: bash

    $ yum install bzip2 bzip2-devel bzip2-libs

**Download 2.5.4 from python.org**

.. code-block:: bash

    $ wget http://python.org/ftp/python/2.5.4/Python-2.5.4.tar.bz2
    $ tar -xvjf Python-2.5.4.tar.bz2
    $ cd Python-2.5.4

**switch to root:**

.. code-block:: bash

    $ ./configure
    $ make
    $ make altinstall

Once complete (this will take a few minutes) rerun the steps above and then you should be good.

**go back to where you untared the mercurial bundle**

.. code-block:: bash

    $ cd mercurial-1.5.1
    $ make PYTHON=python2.5 install

Check to make sure you are running 1.5.1

.. code-block:: bash

    $ hg --version
         Mercurial Distributed SCM (version 1.5.1)

That is all, now you are running Mercurial 1.5.1 on RHEL5 with python2.5!

