Assetto Corsa Server Manager
============================

This is a Django-powered application for managing the configuration and execution of Assetto Corsa servers.


Project Status
--------------

Very much a work-in-progress at this stage; if you stumble across this project please don't use it just yet :)


TODO
----

* create systemd services for acServer and stracker (and implement control/visibility of these services in the ACServerManager ui)
* add minor-rating
* either migrate from sqlite to postgres, or properly configure selinux so apache can write the django sqlite db
* write a bespoke ui for configuring session presets etc (something that mirrors the behaviour of the native windows ACServerManager ui, or at least something more intuitive than the django-admin ui)
* implement bookings (presently only pickup mode works to some extent)
* use apache to proxy to the stracker http ui - this will need modifications to stracker's http_templates though since static asset paths are absolute.
