
:date: 2011-12-31 13:26:42
:tags: django,djangocms,dotcloud,paas
:category: blog
:slug: installing-djangocms-dotcloud-12-easy-steps
:author: Ken Cochrane
:title: Installing DjangoCMS on dotCloud in 12 easy steps

Do you want to use Django-cms on dotcloud but don't know where to start? All you need to do is follow these 12 easy steps, they will get you on your way.


1. Create a place to store your project

    $ mkdir -p ~/projects

2. Go into the projects directory

    $ cd ~/projects

3. Clone git repo from github, requires git client.

    $ git clone git://github.com/kencochrane/django-cms-dotcloud.git
    
4. Go into the new project directory
    
    $ cd django-cms-dotcloud

5. Creating the virtualenv (using virtualenvwrapper, virtualenv, and pip)

    $ mkvirtualenv --no-site-packages --distribute django-cms-dotcloud

6. Installing the dotCloud client  http://docs.dotcloud.com/firststeps/install/ (here are the steps for Linux and Mac OSX)

    $ sudo pip install -U dotcloud

7. Sign up for a dotcloud account https://www.dotcloud.com/accounts/register/ if you haven't already.

8. The first time you use the dotcloud account you will need to add your api key. So type dotcloud and follow the steps. You can find your API key at http://www.dotcloud.com/account/settings

    $ dotcloud

9. Create your dotcloud application

    $ dotcloud create mycmsapp

10. Push your code into dotcloud

     $ dotcloud push mycmsapp .

11. Find out your application url.

     $ dotcloud url mycmsapp

12. Open url in your browser and start using djangoCMS on dotcloud.

13. Optional: If you don't like the URL they gave you, you can use your custom domain. Assuming your application was ramen.www and your domain was www.example.com you would do the following.

     $ dotcloud alias add ramen.www www.example.com


Once you get comfortable with how things work, you could add more plug-ins, create your own custom templates and then change your DEBUG setting to False. So go ahead `fork my project on github <https://github.com/kencochrane/django-cms-dotcloud/fork>`_  and get started.

After you make changes to your local project directory, you can test it on the server by running the dotcloud push command again.

For more info about dotcloud and django-cms and what you can do with with it. check out their docs
 - http://docs.dotcloud.com/firststeps/platform-overview/
 - https://www.django-cms.org/en/documentation/
 
**Links:**
 - **dotcloud** : http://dotcloud.com
 - **Virtualenv** : http://pypi.python.org/pypi/virtualenv
 - **pip** : http://www.pip-installer.org/
 - **virtualenvwrapper** : http://www.doughellmann.com/projects/virtualenvwrapper/
 - **git** : http://git-scm.com/
 


