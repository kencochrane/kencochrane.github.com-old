
:date: 2011-12-30 13:49:26
:tags: python,deployment,hosting
:category: blog
:slug: standardizing-python-wsgi-deployment
:author: Ken Cochrane
:title: Standardizing Python WSGI deployment


Over the past year I have been testing all of the new python platform as a service companies that have popped up, and I have posted my notes on my blog so that everyone can learn from my experiences.  `ep.io <http://kencochrane.net/blog/2011/04/my-experiences-with-epio/>`_, `apphosted.com <http://kencochrane.net/blog/2011/05/apphosted-com-django-hosting-review/>`_, `gondor.io <http://kencochrane.net/blog/2011/04/my-day-gondorio/>`_, `dotcloud.com <http://kencochrane.net/blog/2011/04/deploying-my-django-application-to-dotcloud/>`_, `DjangoZoom.com <http://DjangoZoom.com>`_, `Heroku <http://kencochrane.net/blog/2011/11/developers-guide-for-running-django-apps-on-heroku/>`_, `Django hosting roundup <http://kencochrane.net/blog/2011/06/django-hosting-roundup-who-wins/>`_, 

All and all, the platforms were very similar, they allowed you to easily host your python/django project without having to worry about managing a server or other typical system administration duties. Some of the services were more advanced and had more features then others, but since it was still early in the game, that was expected.  

The one thing that was different between each service was the way that you have your python project setup.  This might not seem like a big deal, but because of the little differences between providers it required me to change my test project every time I wanted to test out a new providers service. These little changes weren't a big deal for me, but it could be a barrier of entry for less technical people. It also makes it harder for someone to change services if they wanted. This probably sounds like a good idea to the platform providers because it makes it a little harder for people to leave their service, but I don't think that was their intention. Looking at the different platforms, and their implementations, you can see they all make sense, and it was just their own way of solving a problem because there was no standard available. 

Before I started programmed in python, I came from a Java background. In Java they have already solved the deployment problem with their WAR files. For those of you that aren't familiar with Java or WAR files, basically WAR files are just java projects that are laid out in a common directory structure, with a few required configuration files (web.xml, etc) that the application server uses when deploying the application. This directory structure is then zipped up for easy portability. All of the different Java application servers know how to read these files and deploy the applications. It makes installing applications really easy, and if you ever need to change application servers, it shouldn't require any changes at all, assuming you stuck with the standard format. `Java WAR files on Wikipedia <http://en.wikipedia.org/wiki/WAR_file_format_(Sun)>`_

I was lucky enough to attend DjangoCon US 2011 in Portland Oregon this year. At the conference there was a Django Hosting Panel moderated by Sean O'Connor where the different hosting providers were asked questions about their platforms. If you didn't get a chance to see it, it is available on blip.tv here. http://blip.tv/djangocon/django-hosting-panel-5572201 *Fun Fact: That is me in the front row with the blue shirt and green hat.*

During the panel, Sean asked if there was any plans for working on interoperability between the different platforms. Andrew Godwin referenced Java's WAR format and also talked about how he has already started to talk to others about this idea at DjangoCon EU and would like to see it move forward. The others in the panel seemed to agree that something could be done, but it didn't seem like it was urgent to them, or if they really cared/wanted to do it. I can understand their reluctance, because I'm sure they have more important things to work on, and this would be very low on their list of things to do. After all whatever comes from this, is going to require changes to their platform in order to support it. 

That is why I think we (the developer community), need to come up with a standard, propose it to the rest o the python community, with input from the different platform providers, and then leave it up to the different providers to decide if they are going to support it or not. It would be great if everyone supported it, but because this isn't going to make anyone money in the short term, it will be hard to force anyone to do it. 

I'm willing to help to create the standard, but where do we start, and whom do we submit the proposal too, the PSF?

I think the easiest place to start would be to look at the different platforms and find out what they have in common, and go from there. Off the top of my head, I'm pretty sure they all support virtualenv and pip for requirements. They are also all wsgi based, but I think that is where the commonality stops. 

For example they all have a different way for specifying application settings. ep.io has an ini file, dotcloud has a yml file, and gondor has a .gondor/config file. It shouldn't be too hard to come up with a standard format with sane attributes.

We could probably all agree on a common project structure, and where to put the common files (requirements.txt for pip requirements and put it in the root of the project, etc.).

Something that will be important is to make the standard solid but flexible. Since all of these platforms are a little different we will need to allow some way for them to have a custom section or file that will be platform dependent, so that they can extend the standard without breaking it. These extensions won't be supported by everyone, but it will allow the platform providers the flexibility to move forward without getting held back with a standard process which is normally a slow process. 

That is also why versioning is important, make sure it is obvious which version of the standard the application is using, so that it doesn't break as changes in the standard are made in the future. 

As you can see, with a little bit of effort I have a nice start, but where do we go from here? What do you think, is this a good idea? Do you want to help move it forward? Post some comments below, and lets continue this discussion into 2012.


