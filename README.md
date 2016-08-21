Assetto Corsa Server Manager
============================

This is a Django-powered application for managing the configuration and execution of Assetto Corsa servers.


Project Status
--------------

Very much a work-in-progress at this stage; if you stumble across this project please don't use it just yet :)


TODO
----

* provide a MORE OBVIOUS way to clone presets as...
* show/hide "advanced" preset fields
* ensure full help_text on models
* revisit model validation
* hook-up "launch server configuration" links to the publish_preset method and provide some feedback on service restarts/status
* add minor-rating
* automate stracker package bundle, acserver content artifacts and ACServerManager db fixtures
  - ideally: a python script which can run on a windows host to gather artifacts for both stracker, ACServerManager (database) and for the acserver's cars/tracks contents directory
  - find a way to import stracker's artifacts (either dissect the http form's underlying method, or maybe use a local http post with ansible?)
* use apache to proxy to the stracker http ui - this will need modifications to stracker's http_templates though since static asset paths are absolute.
* migrate to postgres?
