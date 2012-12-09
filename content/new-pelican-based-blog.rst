:date: 2012-12-09 3:17:48
:tags: pelican,blog
:category: blog
:slug: new-pelican-based-blog
:author: Ken Cochrane
:title: New Pelican Based Blog

I have recently changed my Django based blog to a statically generated blog based on `Pelican <http://getpelican.com>`_, and hosted by `GitHub Pages <http://pages.github.com>`_. This is for a couple of reasons. 

The first reason was because my blog is really simple, it was just a bunch of reStructuredText documents that were converted to HTML. I didn't need the Django-admin features and I always felt it was a little overkill for my blog. 

The second reason was because I wanted to host my blog contents on GitHub so that others could change/update/edit my blog posts and send me pull requests if they have something good to add. Doing this with my old blog would have been hard, but it will be really easy with this current setup.

I was looking through all of the different static generators, and boy there are a lot of them. I decided to pick pelican because it did what I needed, and was real easy to setup and use. 

My requirements for a site generator:

1. Python: I wanted it python based, in case it needed any changes, I wouldn't need much of a learning curve learning a new language.

2. Open Source: I wanted to have the ability to change it to add my own features in case it doesn't have them to start. Plus Open Source code rules.

3. reStructureText: I wanted to write my blog posts in ReST.

4. Themes: I wanted some out of the box themes that I could pick from and customize

5. Easy: I wanted something with minimum setup and overhead to get started.

6. Maintain Links: I wanted to keep the same URL structure from my old blog so I wouldn't get lots of 404 errors once I converted. 

7. Active development: I wanted a project that is currently under active development.

After I did some quick searches, I found Pelican, and I liked what I saw. I wrote a simple python script that pull out my blog posts from my old blog and generated the initial ReST docs, which got me most of the way there.

Once I got the content pulled out, I just needed to pick a theme, and configure the settings. Then setup my github pages site, and push all the code. The last change was to change my DNS records, and then I was done. 

Now anytime I want to write a blog post, all I have to do is add a new ReST doc and rerun the build command, and commit my changes, and push my repo. Then github automatically updates my site. Simple as that.

I'll run it from github for a little while and see how I like it. I might end up changing hosting, since github has very limited features, and doesn't allow you to add any rewrite rules or anything custom. I could have just as easily hosted on AWS s3, or `dotCloud <http://dotCloud.com>`_, but I wanted to try this out first since it was pretty easy to setup.

If you switched to a static site generator, or are thinking about doing it, let me know what you think and what tools you are using. 