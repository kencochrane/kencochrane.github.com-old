:date: 2013-05-12 12:41:48
:tags: rackspace, kernel, ubuntu
:category: blog
:slug: upgrading-linux-kernel-ubuntu-rackspace-cloud
:author: Ken Cochrane
:title: Upgrading the Ubuntu linux kernel on Rackspace cloud

Yesterday I wrote a `blog post <|filename|/content/running-docker-on-rackspace-cloud.rst>`_ on how to install `Docker <http://www.docker.io>`_ on to `RackSpace Cloud <http://www.rackspace.com/cloud/servers/>`_, and one of the steps was to upgrade the kernel to the lastest one so that Docker would be nice and stable. The problem that I found out was that there wasn't much information how to upgrade the kernel on the Rackspace Cloud servers, so I thought I would put the steps here.

The goal here is to upgrade Ubuntu 12.04 and 12.10 so that it has the same kernel as 13.04. Here are the steps.

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

5. Install the 3.8.x kernel using the PPA

    .. code-block:: bash
        
        # install the new kernel
        $ apt-get install linux-generic-lts-raring
        
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

6. Reboot server (either via command line or console)

7. login again and check to make sure the kernel was updated

    .. code-block:: bash
        
        $ ssh root@<server_ip>
        $ uname -a
        Linux docker-12-04 3.8.0-19-generic #30~precise1-Ubuntu SMP Wed May 1 22:26:36 UTC 2013 x86_64 x86_64 x86_64 GNU/Linux
        
        # nice 3.8.


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

5. Install the 3.8.x kernel using the ubuntu-x-swat PPA

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

6. Reboot server (either via command line or console)

7. login again and check to make sure the kernel was updated

    .. code-block:: bash
        
        $ ssh root@<server_ip>
        $ uname -a
        Linux docker-12-10 3.8.0-19-generic #29~precise2-Ubuntu SMP Fri Apr 19 16:15:35 UTC 2013 x86_64 x86_64 x86_64 GNU/Linux
        
        # nice 3.8.
