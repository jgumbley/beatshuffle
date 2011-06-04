class pythonweb {
  package { "httpd":
    ensure => present,
  }

  service { "httpd":
    ensure => running,
    require => Package["httpd"],
  }
}

# need to add scipts already made for mod_wsgi and python
# but need to get source for modules from work pc 

package { "postgresql90-server":
    ensure => present,
    require => Yumrepo["postgres"],
    }

service { "postgresql-90":
    ensure => running,
    require => Package["postgresql90-server"],
    }

yumrepo { "postgres":
      baseurl => "http://yum.pgrpms.org/9.0/redhat/rhel-5-x86_64/", 
      descr => "Postgres Repo",
      enabled => 1,
      gpgcheck => 0
   }


include pythonweb 

