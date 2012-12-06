
:date: 2010-05-14 16:34:38
:tags: linux,memcached,RHEL5,install,script
:category: blog
:slug: Automated-Install-Script-for-memcached-on-RHEL5
:author: Ken Cochrane
:title: Automated Install Script for memcached on RHEL5


I created this script that will download memcached build,install and set it up to start up automatically on reboot. It also installs the init.d script to manage memcache so you can restart etc.

You can either copy and paste it into your shell prompt using a user that has install privileges (root,admin,etc) or you can copy into a .sh file and execute it.

The code for most of this was take from this blog post: http://www.vbseo.com/blogs/danny-bembibre/daemon-scripts-memcached-44/ it doesn't seem to be around anymore so I put it here for anyone else looking for this very helpful info.

.. code-block:: bash

    wget http://memcached.googlecode.com/files/memcached-1.4.5.tar.gz
    tar -xvzf memcached-1.4.5.tar.gz
    cd memcached-1.4.5
    ./configure
    make
    make test
    make install

    touch /etc/memcached.conf
    cat << EOF >> /etc/memcached.conf
    #Memory a user
    -m 64
    # default port
    -p 11211
    # user to run daemon nobody/apache/www-data
    -u nobody
    # only listen locally
    -l 127.0.0.1
    EOF

    touch /etc/init.d/memcached
    chmod +x /etc/init.d/memcached

    cat << EOF >> /etc/init.d/memcached
    #!/bin/bash
    #
    # memcached    This shell script takes care of starting and stopping
    #              standalone memcached.
    #
    # chkconfig: - 80 12
    # description: memcached is a high-performance, distributed memory
    #              object caching system, generic in nature, but
    #              intended for use in speeding up dynamic web
    #              applications by alleviating database load.
    # processname: memcached
    # config: /etc/memcached.conf
    # Source function library.
    . /etc/rc.d/init.d/functions
    PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
    DAEMON=/usr/local/bin/memcached
    DAEMONBOOTSTRAP=/usr/local/bin/start-memcached
    DAEMONCONF=/etc/memcached.conf
    NAME=memcached
    DESC=memcached
    PIDFILE=/var/run/$NAME.pid
    [ -x $DAEMON ] || exit 0
    [ -x $DAEMONBOOTSTRAP ] || exit 0
    RETVAL=0
    start() {
     echo -n $"Starting $DESC: "
     daemon $DAEMONBOOTSTRAP $DAEMONCONF
     RETVAL=$?
     [ $RETVAL -eq 0 ] && touch $PIDFILE
     echo
     return $RETVAL
    }
    stop() {
     echo -n $"Shutting down $DESC: "
     killproc $NAME
     RETVAL=$?
     echo
     [ $RETVAL -eq 0 ] && rm -f $PIDFILE
     return $RETVAL
    }
    # See how we were called.
    case "$1" in
     start)
      start
      ;;
     stop)
      stop
      ;;
     restart|reload)
      stop
      start
      RETVAL=$?
      ;;
     status)
      status $prog
      RETVAL=$?
      ;;
     *)
      echo $"Usage: $0 {start|stop|restart|status}"
      exit 1
    esac
    exit $RETVAL
    EOF

    touch /usr/local/bin/start-memcached
    chmod +x /usr/local/bin/start-memcached

    cat << EOF >> /usr/local/bin/start-memcached
    #!/usr/bin/perl -w
    # start-memcached
    # 2003/2004 - Jay Bonci <jaybonci@debian.org>
    # This script handles the parsing of the /etc/memcached.conf file
    # and was originally created for the Debian distribution.
    # Anyone may use this little script under the same terms as
    # memcached itself.
    use strict;
    if ($> != 0 and $< != 0) {
     print STDERR "Only root wants to run start-memcached.\n";
     exit;
    }
    my $etcfile = shift || "/etc/memcached.conf";
    my $params = [];
    my $etchandle; 
    # This script assumes that memcached is located at /usr/bin/memcached, and
    # that the pidfile is writable at /var/run/memcached.pid
    my $memcached = "/usr/local/bin/memcached";
    my $pidfile = "/var/run/memcached.pid";
    # If we don't get a valid logfile parameter in the /etc/memcached.conf file,
    # we'll just throw away all of our in-daemon output. We need to re-tie it so
    # that non-bash shells will not hang on logout. Thanks to Michael Renner for 
    # the tip
    my $fd_reopened = "/dev/null";
    sub handle_logfile {
     my ($logfile) = @_;
     $fd_reopened = $logfile;
    }
    sub reopen_logfile {
     my ($logfile) = @_;
     open *STDERR, ">>$logfile";
     open *STDOUT, ">>$logfile";
     open *STDIN, ">>/dev/null";
     $fd_reopened = $logfile;
    }
    # This is set up in place here to support other non -[a-z] directives
    my $conf_directives = {
     "logfile" => \&handle_logfile
    };
    if (open $etchandle, $etcfile) {
     foreach my $line (<$etchandle>) {
      $line =~ s/\#.*//go;
      $line = join ' ', split ' ', $line;
      next unless $line;
      next if $line =~ /^\-[dh]/o;
      if ($line =~ /^[^\-]/o) {
       my ($directive, $arg) = $line =~ /^(.*?)\s+(.*)/; 
       $conf_directives->{$directive}->($arg);
       next;
      }
      push @$params, $line;
     }
    }
    unshift @$params, "-u root" unless (grep $_ eq '-u', @$params);
    $params = join " ", @$params;
    if (-e $pidfile) {
     open PIDHANDLE, "$pidfile";
     my $localpid = <PIDHANDLE>;
     close PIDHANDLE;
     chomp $localpid;
     if (-d "/proc/$localpid") {
      print STDERR "memcached is already running.\n"; 
      exit;
     } else {
      `rm -f $localpid`;
     }
    }
    my $pid = fork();
    if ($pid == 0) {
     reopen_logfile($fd_reopened);
     exec "$memcached $params";
     exit(0);
    } elsif (open PIDHANDLE,">$pidfile") {
     print PIDHANDLE $pid;
     close PIDHANDLE;
    } else {
     print STDERR "Can't write pidfile to $pidfile.\n";
    }
    EOF

    /etc/init.d/memcached restart
    /sbin/chkconfig memcached on

