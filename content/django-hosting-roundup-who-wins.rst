:date: 2011-06-06 22:03:59
:tags: django,hosting,apphosted,python,deployment,dotcloud,epio,gondor,djangozoom,heroku,paas
:category: blog
:slug: django-hosting-roundup-who-wins
:author: Ken Cochrane
:title: Django Hosting Roundup: (Ep.io vs Gondor.io vs DotCloud vs Heroku vs AppHosted vs DjangoZoom) Who wins?

Updates
=======
- Updated 2/16/2012: Full disclosure. On Feb 16th 2012, I accepted a job with dotCloud. I plan on keeping this blog post up to date and impartial. If you think there are any errors, please let me know in the comments below. 

- Updated 1/26/2012: Updated Gondor.io with info from Donald Stufft. 

- Updated 01/24/2012: changed gondor.io to include SSL support

- Updated 01/01/2012: Added Heroku and updated ep.io, gondor.io, and dotcloud.


Intro
=====
For the past 6 weeks I have been trying out all of the new django/python hosting services that are currently available today, and I have been writing about my experiences along the way. It only makes sense to conclude this series of articles with one last article comparing all of the services against each other. It is important to note that many of these services are still in development and aren't even available to the general public, so I'll try to keep this article up to date as these services change over time. With that said, don't take my word for it, go out and try all of these services on your own and find out which one you like the best, you won't be disappointed.


Quick Recap
===========

ep.io
-----
Blog post: `My Experiences with ep.io <http://kencochrane.net/blog/2011/04/my-experiences-with-epio/>`_

Pretty solid offering, with a nice set of features and a decent price. Good set of documentation.

[**Update**: Epio closed down on May 31st 2012 ]

gondor.io
----------
Blog post: `My day in gondor.io <http://kencochrane.net/blog/2011/04/my-day-gondorio/>`_

Their website has a nice list of features that they expect to have once they officially launch, but most of those features aren't available yet. The documentation is a little light, but the service has a lot of potential. 

dotCloud.com
------------
Blog post: `Deploying my Django application to dotcloud.com <http://kencochrane.net/blog/2011/04/deploying-my-django-application-to-dotcloud/>`_

They have a ton of money ($10M), and with it, a ton of features. They are very developer friendly, but you need to be pretty technical, it isn't quite ready for beginners. Good set of documentation.

[**Full disclosure**: I now work for dotCloud]

AppHosted.com
-------------
Blog post: `apphosted.com Django Hosting Review <http://kencochrane.net/blog/2011/05/apphosted-com-django-hosting-review/>`_

Built with security, stability and scalability on their mind from the beginning. They have a solid offering, and they look to be targeting enterprise customers who will pay more for that peace of mind.  They are currently lacking some key features, which I'm sure they will be adding soon.  Good set of documentation.

DjangoZoom.com
--------------
Blog post: `DjangoZoom.com Review <http://kencochrane.net/blog/2011/06/djangozoom-com-review/>`_

Built to be fast and easy to use, still missing some key features, but I'm sure they will be available by the time they go live. Decent amount of documentation.

Heroku.com
----------
Blog post: `Developers guide for running django apps on Heroku <http://kencochrane.net/blog/2011/11/developers-guide-for-running-django-apps-on-heroku/>`_

Originally built as a Ruby on Rails service, they have now added support for python. The service is still in beta, but it has a lot of potential. It looks a lot like what dotCloud is offering, with the ability to run code from almost any language, and a ton of different add-ons for lots of different services.


Awards
======

Fastest Deployments:
--------------------
`DjangoZoom.com <http://DjangoZoom.com>`_ - Zoom is right, it doesn't take long to configure your application and have it up and running on their servers.

Easiest To Use:
---------------
`DjangoZoom.com <http://DjangoZoom.com>`_ - No command line interface needed, just a web browser, a project in a git repo that it has access too, and a few questions answered and your app is up and running.

Most Features:
--------------
`dotCloud.com <http://dotcloud.com>`_ - They raised $10 Million, and they are spending it on hiring people, buying companies, and building services. They have a bunch of services currently and they don't plan on stopping, their roadmap has everything on it, and I think if you give them enough time they will eventually have a service for everything.

Most Developer Friendly:
------------------------
`dotCloud.com <http://dotcloud.com>`_ - They give lots of features without handcuffing the developer. They are the only company with full database and shell access. They do a good job of offering the same type of service a developer could get if they built it themselves.

Best Overall Value:
-------------------
`ep.io <http://ep.io>`_ - This one is hard since most of the services don't have any pricing listed, but currently ep.io is in the lead, they offer reasonable prices with a nice Free tier. This allows developers to try out the service for FREE, as well as run smaller pet projects that they might not have tried before because they didn't want to pay for hosting. They have the second most features available, second to only dotCloud, and there service is pretty solid.

Easiest Project Setup:
----------------------
`apphosted.com <http://apphosted.com>`_ - Their goal was to make it real easy to get your project up onto their servers without having to change your project, and they did that, there was very little if any changes I needed to make in order to get my application up on their servers.


Django Feature Hosting Matrix
=============================

To make things easier when comparing all of the different services I have built this matrix with all of the information I compiled from each of the services. I don't know the answers for all services, but I'll update it when I find out those answers. If you know the answers feel free to post a comment to let me know. 

I have included all of the new django services as well as google app engine and webfaction.com, a tradition hosting service. This should make it a little easier to see how these new services compare to other hosting options.

.. html::

    <iframe width='775' height='500' frameborder='0' src='https://docs.google.com/spreadsheet/pub?key=0AtuyQoTrXCavdDdyQ1RCX29FcDhQeDgzMXp0NGpGeWc&single=true&gid=0&output=html&widget=true'></iframe>

Who wins?
=========
It is really hard to pick just one winner,  mainly because most of these services are still in beta and not quite finished yet. Also because each service is a little different, and it will depend on what you are trying to do. So, go out try them out, and let me know which one you picked. 

The real winner is us, the developers, and the python community in general. We now have a bunch of really cool services that will make our lives better, and that is awesome. 

Thank you!
==========
I want to thank all of the people who made these services, and gave me early access to their systems so that I could play around with them. I wish them the best of luck, and hope they all are really successful, and they are around for a long time.
