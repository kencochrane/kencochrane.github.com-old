:date: 2015-02-15 11:05:01
:tags: django,python,defender,redis
:category: blog
:slug: introducing-django-defender
:author: Ken Cochrane
:title: Introducing Django Defender


Normally websites do very few logins, someone logs in once and their session
is good for a bunch of hours. Since it's a one time thing, it doesn't matter
if it isn't very fast. At `Docker <https://www.docker.com>`_ our authentication
system handles requests for both the `Docker Hub <https://hub.docker.com>`_,
as well as all Docker Engine commands that interact with the Docker Hub
(docker push, pull, etc). This Authentication system handles thousands of login
attempts every minute, so any slow down in the login process has a large impact
on our system.

We are always looking at ways to improve the security of our systems, and one of
the things we looked at implementing was a way to prevent brute force login attempts.
The first thing we did was look to see if there was an open source solution
available that would do what we needed. The Docker Hub along with the
authentication system is written in Python using `Django <http://www.djangoproject.com>`_
.
So we did some research to see what was the best solution available to us. We quickly
came to `django-axes <https://github.com/django-pci/django-axes>`_, which is a great library, and had everything we were looking for. Best of all, it wasn't that hard to add to our system.

When we started using django-axes our
traffic was pretty normal, but with the explosive growth of Docker we have seen
a huge increases in traffic. As the traffic increased, we started noticing that
login times were slowing down. Upon further inspection we noticed that with
django-axes turned on it was adding a 200 to 300ms overheard compared to when it
was turned off. We did some more digging to see what was causing all of the
delay, and we found out the reason is because django-axes stores all of its
information in the database and in order to determine if someone is blocked you
need to do a bunch of queries, and the more login attempts, the larger the axes database
tables get, and thus the queries get slower, and in turn slows down the login process.

Our first attempts to speed things up was to add more database indexes,
and to run a script that kept the axes database tables small. This worked for a
little while, but as the traffic increased, it stopped working. It was quickly
determined that we would need to replace django-axes. We looked around at other
brute force libraries, and there was nothing that offered what we needed for
features, was fast, and well maintained.

Since we couldn't find anything, I started working on a replacement. On one of my
many cross country flights, I started working on a replacement. In order to make
the process quicker, it started as a fork of django-axes, where I removed the
stuff we didn't need, and then replaced the slow parts with faster ones. The
main goal was to avoid hitting the database in order to determine if the user
was blocked. Since we are big fans of `Redis <http://redis.io>`_, and we were using it
in other places already, we decided to use Redis as our backend for storing all
of our data for determining if someone is blocked. We also allow the logging of
login attempts to the database, but to speed things up, we defer this to a
background celery task.

After a few cross country flights, and some help from some of my co-workers, we
now have a library, that we are using on the Docker Hub. We have been using it
for about a month now, and the results have been great. With this new library we are
seeing under a 10ms impact on our logins, which is really great. We are able to
have the features we need without the overhead.

Now that we have proven the project to be successful, we have decided to open
source the library, so that others can also use it, and contribute back any features
or improvements they might find important.

So without further ado, I'm proud to introduce `Django Defender <https://github.com/kencochrane/django-defender>`_, a brute force
login preventions library built for speed.

We have labeled the first version 0.1, but it is very stable and already
production ready. We have very good code coverage (95%+) and we have tests
and support for a number of different Python and Django versions.

We also have django admin pages that can be used to manage the blocked users
and IP addresses.

Please try it out, and let us know if you have any questions.

Links:
------

- **Source code**: https://github.com/kencochrane/django-defender
- **PyPi**: https://pypi.python.org/pypi/django-defender


Version Support:
----------------

- **Python**: 2.6.x, 2.7.x, 3.3.x, 3.4.x, PyPy
- **Django**: 1.6.x, 1.7.x

What's in 0.1:
--------------

- Configurable: When to block, What to do when blocked.
- Uses Redis for data store.
- Blocking IP and usernames when too many login attempts
- Logging of access attempts to database.
- Celery for writing access attempt logs to the database in the background
- Admin pages (integrated with Django admin), to manage the blocked IP's and usernames.

How to install:
---------------

   ``pip install django-defender``


Admin Screen shots:
-------------------

.. image:: https://cloud.githubusercontent.com/assets/261601/5950540/8895b570-a729-11e4-9dc3-6b00e46c8043.png

.. image:: https://cloud.githubusercontent.com/assets/261601/5950541/88a35194-a729-11e4-981b-3a55b44ef9d5.png
