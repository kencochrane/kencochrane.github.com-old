
:date: 2011-12-31 14:25:11
:tags: django,djangocms,heroku,paas
:category: blog
:slug: installing-djangocms-on-heroku-in-13-easy-steps
:author: Ken Cochrane
:title: Installing DjangoCMS on Heroku in 13 easy steps

Do you want to use Django-cms on Heroku but don't know where to start? All you need to do is follow these 13 easy steps, and they will get you on your way.


1. Create a place to store your project

    $ mkdir -p ~/projects

2. Go into the projects directory

    $ cd ~/projects

3. Clone git repo from github, requires git client.

    $ git clone git://github.com/kencochrane/django-cms-heroku.git
    
4. Go into the new project directory
    
    $ cd django-cms-heroku

5. Creating the virtualenv (using virtualenvwrapper, virtualenv, and pip)

    $ mkvirtualenv --no-site-packages --distribute django-cms-heroku

6. Sign-Up for a Heroku account. https://api.heroku.com/signup

7. Install the Heroku client. http://devcenter.heroku.com/articles/quickstart

8. The first time you use the Heroku client you will need to login using the same information you used when you signed up. Follow the prompts, and it will finish your install.

    $ heroku login

9. Create your heroku application

    $ heroku create --stack cedar

10. Push your code into heroku

     $ git push heroku master

11. Sync your database and create your admin account.

     $ heroku run python mycms/manage.py syncdb --all

12. Run your database migrations.
    
     $ heroku run python mycms/manage.py migrate --fake

13. Open application in your browser and start using djangoCMS on heroku.

     $ heroku open


Once you get comfortable with how things work, you could add more plug-ins, create your own custom templates and then change your DEBUG setting to False. So go ahead `fork my project on github <https://github.com/kencochrane/django-cms-heroku/fork>`_  and get started.

After you make changes to your local project directory, you can test it on the server by running the git push command again.

For more info about Heroku and django-cms and what you can do with with it. check out their docs
 - http://devcenter.heroku.com/categories/platform-basics
 - https://www.django-cms.org/en/documentation/

Links:
 - **Virtualenv** : http://pypi.python.org/pypi/virtualenv
 - **pip** : http://www.pip-installer.org/
 - **virtualenvwrapper** : http://www.doughellmann.com/projects/virtualenvwrapper/
 - **git** : http://git-scm.com/
 


