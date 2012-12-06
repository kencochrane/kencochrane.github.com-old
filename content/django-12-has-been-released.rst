
:date: 2010-05-17 16:12:11
:tags: django,python
:category: blog
:slug: django-12-has-been-released
:author: Ken Cochrane
:title: Django 1.2 has been Released!

============================
Django 1.2 has been released
============================

I have been waiting for this release for a while now, mostly because it includes some of the features I have been dying to get my hands on. The ones I like the most are

* support for multiple databases
* smart-if template tag
* The new Email Backends
* relaxed requirements for usernames.

Here is a list for some of the features, and a little bit about each one.

Support for multiple databases
--------------------------------
 Django 1.2 adds the ability to use more than one database in your Django project. Queries can be issued at a  specific database with the using() method on QuerySet objects. Individual objects can be saved to a specific  database by providing a using argument when you call save().

Model validation
------------------
 Model instances now have support for validating their own data, and both model and form fields now accept configurable lists of validators specifying reusable, encapsulated validation behavior. Note, however, that validation must still be performed explicitly. Simply invoking a model instance’s save() method will not perform any validation of the instance’s data.

Improved CSRF protection
--------------------------
 Django now has much improved protection against Cross-Site Request Forgery (CSRF) attacks. This type of attack occurs when a malicious Web site contains a link, a form button or some JavaScript that is intended to perform some action on your Web site, using the credentials of a logged-in user who visits the malicious site in their browser. A related type of attack, “login CSRF,” where an attacking site tricks a user’s browser into logging into a site with someone else’s credentials, is also covered.

Messages framework
------------------
 Django now includes a robust and configurable messages framework with built-in support for cookie- and session-based messaging, for both anonymous and authenticated clients. The messages framework replaces the deprecated user message API and allows you to temporarily store messages in one request and retrieve them for display in a subsequent request (usually the next one).

Object-level permissions
------------------------
 A foundation for specifying permissions at the per-object level has been added. Although there is no implementation of this in core, a custom authentication backend can provide this implementation and it will be used by django.contrib.auth.models.User. See the authentication docs for more information.

Permissions for anonymous users
-------------------------------
 If you provide a custom auth backend with supports_anonymous_user set to True, AnonymousUser will check the backend for permissions, just like User already did. This is useful for centralizing permission handling - apps can always delegate the question of whether something is allowed or not to the authorization/authentication backend. See the authentication docs for more details.

Relaxed requirements for usernames
----------------------------------
 The built-in User model’s username field now allows a wider range of characters, including @, +, . and - characters.

E-mail backends
---------------
 You can now configure the way that Django sends e-mail. Instead of using SMTP to send all e-mail, you can now choose a configurable e-mail backend to send messages. If your hosting provider uses a sandbox or some other non-SMTP technique for sending mail, you can now construct an e-mail backend that will allow Django’s standard mail sending methods to use those facilities. This also makes it easier to debug mail sending. Django ships with backend implementations that allow you to send e-mail to a file, to the console, or to memory. You can even configure all e-mail to be thrown away.

“Smart” if tag
--------------
 The if tag has been upgraded to be much more powerful. First, we’ve added support for comparison operators. The operators supported are ==, !=, <, >, <=, >=, in and not in, all of which work like the Python operators, in addition to and, or and not, which were already supported.

Template caching
----------------
 In previous versions of Django, every time you rendered a template, it would be reloaded from disk. In Django 1.2, you can use a cached template loader to load templates once, then cache the result for every subsequent render. This can lead to a significant performance improvement if your templates are broken into lots of smaller subtemplates (using the {% extends %} or {% include %} tags). As a side effect, it is now much easier to support non-Django template languages. For more details, see the notes on supporting non-Django template languages.

Natural keys in fixtures
------------------------
 Fixtures can now refer to remote objects using Natural keys. This lookup scheme is an alternative to the normal primary-key based object references in a fixture, improving readability and resolving problems referring to objects whose primary key value may not be predictable or known.

Fast failure for tests
----------------------
 Both the test subcommand of django-admin.py and the runtests.py script used to run Django's own test suite now support a --failfast option. When specified, this option causes the test runner to exit after encountering a failure instead of continuing with the test run. In addition, the handling of Ctrl-C during a test run has been improved to trigger a graceful exit from the test run that reports details of the tests that were run before the interruption.

BigIntegerField
---------------
 Models can now use a 64-bit BigIntegerField type.

Improved localization
---------------------
 Django's internationalization framework has been expanded with locale-aware formatting and form processing. That means, if enabled, dates and numbers on templates will be displayed using the format specified for the current locale. Django will also use localized formats when parsing data in forms. See Format localization for more details.

readonly_fields in ModelAdmin
-----------------------------
 django.contrib.admin.ModelAdmin.readonly_fields has been added to enable non-editable fields in add/change pages for models and inlines. Field and calculated values can be displayed alongside editable fields.

And much much more!!
--------------------

* To find out what else is in this release visit `Django 1.2 offical release notes <http://docs.djangoproject.com/en/dev/releases/1.2/>`_.
* Download it here: http://www.djangoproject.com/download/1.2/tarball/
* Offical website: `DjangoProject.com <http://www.djangoproject.com/>`_.

