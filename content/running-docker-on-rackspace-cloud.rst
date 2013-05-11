:date: 2013-05-11 12:17:48
:tags: docker, rackspace, dotcloud
:category: blog
:slug: running-docker-on-rackspace-cloud
:author: Ken Cochrane
:title: Running Docker on Rackspace with Ubuntu

I have been playing with `Docker <http://www.docker.io>`_ a lot lately, and it got me wondering how hard it would be to run Docker on the different Cloud providers. I noticed there were already directions on how to install on `Amazon EC2 <http://docs.docker.io/en/latest/installation/amazon.html>`_ but nothing for the Rackspace Cloud.

If you would like to run `Docker <http://www.docker.io>`_ on the `RackSpace Cloud <http://www.rackspace.com/cloud/servers/>`_ using `Ubuntu <http://www.ubuntu.com/>`_ you're in luck. I just spent the afternoon figuring out how to get it installed on Ubuntu 12.04, 12.10, and 13.04, and I have included my notes below. 13.04 is the easiest to get up and running since it has the most recent kernel, but the others aren't too bad either, they just need a few more steps, to get them up to par.

I would love to expand this to other distros on Rackspace, so if you come up with more, send me a note, and so I can link to them. 

Ubuntu 12.04
------------

1. Build an Ubuntu 12.04 server using the "Next generation cloud servers", with your desired size. It will give you the password, keep that you will need it later.
2. When the server is up and running ssh into the server.

    .. code-block:: bash

        $ ssh root@<server-ip>

3. Once you are logged in you should check what kernel version you are running.

    .. code-block:: bash

        $ uname -a
        Linux docker-12-04 3.2.0-38-virtual #61-Ubuntu SMP Tue Feb 19 12:37:47 UTC 2013 x86_64 x86_64 x86_64 GNU/Linux

4. Let's update the server package list

    .. code-block:: bash

        $ apt-get update

5. Now lets install Docker and it's dependencies. To keep things simple, we will use the Docker install script. It will take a couple of minutes.

    .. code-block:: bash

        $ curl get.docker.io | sudo sh -x

6. Docker runs best with a new kernel, so lets use 3.8.x

    .. code-block:: bash
        
        # add the ppa to get the right kernel package
        $ echo deb http://ppa.launchpad.net/ubuntu-x-swat/r-lts-backport/ubuntu precise main > /etc/apt/sources.list.d/xswat.list
        
        # add the key for the ppa
        $ sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 3B22AB97AF1CDFA9
        
        # update packages again
        $ apt-get update
        
        # install the new kernel
        $ apt-get install linux-image-3.8.0-19-generic
        
        # update grub so it will use the new kernel after we reboot
        $ update-grub
        
        # update-grub doesn't always work so lets make sure. ``/boot/grub/menu.lst`` was updated.
        $ grep 3.8.0- /boot/grub/menu.lst
        
        # nope it wasn't lets manually update ``/boot/grub/menu.lst``  (make sure you are searching for correct kernel version, look at initial uname -a results.)
        $ sed -i s/3.2.0-38-virtual/3.8.0-19-generic/ /boot/grub/menu.lst
        
        # once again lets make sure it worked.
        $ grep 3.8.0- /boot/grub/menu.lst
        title          Ubuntu 12.04.2 LTS, kernel 3.8.0-19-generic
        kernel          /boot/vmlinuz-3.8.0-19-generic root=/dev/xvda1 ro quiet splash console=hvc0
        initrd          /boot/initrd.img-3.8.0-19-generic
        title          Ubuntu 12.04.2 LTS, kernel 3.8.0-19-generic (recovery mode)
        kernel          /boot/vmlinuz-3.8.0-19-generic root=/dev/xvda1 ro quiet splash  single
        initrd          /boot/initrd.img-3.8.0-19-generic
        
        # much better.

7. Reboot server (either via command line or console)
8. login again and check to make sure the kernel was updated

    .. code-block:: bash
        
        $ ssh root@<server_ip>
        $ uname -a
        Linux docker-12-04 3.8.0-19-generic #30~precise1-Ubuntu SMP Wed May 1 22:26:36 UTC 2013 x86_64 x86_64 x86_64 GNU/Linux
        
        # nice 3.8.

9. Make sure docker is running and test it out.

    .. code-block:: bash
        
        $ start dockerd
        $ docker pull busybox
        $ docker run busybox /bin/echo hello world
        hello world

Ubuntu 12.10
------------

1. Build an Ubuntu 12.10 server using the "Next generation cloud servers", with your desired size. It will give you the password, keep that you will need it later.
2. When the server is up and running ssh into the server.

    .. code-block:: bash

        $ ssh root@<server-ip>

3. Once you are logged in you should check what kernel version you are running.

    .. code-block:: bash

        $ uname -a
        Linux docker-12-10 3.5.0-25-generic #39-Ubuntu SMP Mon Feb 25 18:26:58 UTC 2013 x86_64 x86_64 x86_64 GNU/Linux

4. Let's update the server package list

    .. code-block:: bash

        $ apt-get update

5. Now lets install Docker and it's dependencies. To keep things simple, we will use the Docker install script. It will take a couple of minutes.

    .. code-block:: bash

        $ curl get.docker.io | sudo sh -x

6. Docker runs best with a new kernel, so lets use 3.8.x

    .. code-block:: bash
        
        # add the ppa to get the right kernel package
        $ echo deb http://ppa.launchpad.net/ubuntu-x-swat/q-lts-backport/ubuntu quantal main > /etc/apt/sources.list.d/xswat.list
        
        # add the key for the ppa
        $ sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 3B22AB97AF1CDFA9
        
        # update packages again
        $ apt-get update
        
        # install the new kernel
        $ apt-get install linux-image-3.8.0-19-generic

        # make sure grub has been updated.
        $ grep 3.8.0- /boot/grub/menu.lst
        title   Ubuntu 12.10, kernel 3.8.0-19-generic
        kernel  /boot/vmlinuz-3.8.0-19-generic root=/dev/xvda1 ro quiet splash console=hvc0
        initrd  /boot/initrd.img-3.8.0-19-generic
        title   Ubuntu 12.10, kernel 3.8.0-19-generic (recovery mode)
        kernel  /boot/vmlinuz-3.8.0-19-generic root=/dev/xvda1 ro quiet splash  single
        initrd  /boot/initrd.img-3.8.0-19-generic
        
        # looks good. If it doesn't work for you, look at the notes for 12.04 to fix.

7. Reboot server (either via command line or console)
8. login again and check to make sure the kernel was updated

    .. code-block:: bash
        
        $ ssh root@<server_ip>
        $ uname -a
        Linux docker-12-10 3.8.0-19-generic #29~precise2-Ubuntu SMP Fri Apr 19 16:15:35 UTC 2013 x86_64 x86_64 x86_64 GNU/Linux
        
        # nice 3.8.

9. Make sure docker is running and test it out.

    .. code-block:: bash
        
        $ start dockerd
        $ docker pull busybox
        $ docker run busybox /bin/echo hello world
        hello world

Ubuntu 13.04
------------

1. Build an Ubuntu 13.04 server using the "Next generation cloud servers", with your desired size. It will give you the password, keep that you will need it later.
2. When the server is up and running ssh into the server.

    .. code-block:: bash

        $ ssh root@<server-ip>

3. Once you are logged in you should check what kernel version you are running.

    .. code-block:: bash

        $ uname -a
        Linux docker-1304 3.8.0-19-generic #29-Ubuntu SMP Wed Apr 17 18:16:28 UTC 2013 x86_64 x86_64 x86_64 GNU/Linux

4. Let's update the server package list

    .. code-block:: bash

        $ apt-get update

5. Now lets install Docker and it's dependencies. To keep things simple, we will use the Docker install script. It will take a couple of minutes.

    .. code-block:: bash

        $ curl get.docker.io | sudo sh -x

6. Make sure docker is running and test it out.

    .. code-block:: bash
        
        $ start dockerd
        $ docker pull busybox
        $ docker run busybox /bin/echo hello world
        hello world

What's Next
-----------
Now that you have Docker running on a server, you can look at the different `Docker examples <http://docs.docker.io/en/latest/examples/>`_ in the documentation to see how it works, and then build something, and let everyone know what you have built. If you have any issues or suggestions, open a github issue and let everyone know. Docker is a new project, and it is moving quick, so any suggestions that you have might help shape the future of the project. 


