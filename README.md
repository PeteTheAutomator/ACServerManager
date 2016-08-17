Assetto Corsa Server Manager
============================

This is a Django-powered application for managing the configuration and execution of Assetto Corsa servers.


Project Status
--------------

Very much a work-in-progress at this stage; if you stumble across this project please don't use it just yet :)


TODO
----

* provide a way to configure acserver ADMIN passwords (session passwords are implemented)
* provide a MORE OBVIOUS way to clone presets as...
* find a way to automate stracker package bundle
* show/hide "advanced" preset fields
* implement the welcome message
* ensure full help_text on models
* revisit model validation
* hook-up "launch server configuration" links to the publish_preset method and provide some feedback on service restarts/status
* add minor-rating
* implement bookings (presently only pickup mode works to some extent)
* use apache to proxy to the stracker http ui - this will need modifications to stracker's http_templates though since static asset paths are absolute.
* migrate to postgres?
