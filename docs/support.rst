*******
Support
*******
Please understand that I am one person working on this project - for free, when I have a spare moment, in my spare time.

I will do my best to help a friend however, so if you get stuck or if you've any questions please get in touch using the
contact information below.

Project Status
--------------
Right now this project should be considered **Beta**

Roadmap
-------
This really depends on how many others find this project useful - these are the items on the TODO list

* simplify/automate as much as possible (this is ongoing, but I really want to make it trivial to deploy/install)
* enforce the launch of only single instances in the UI (presently it seems you can run multiple servers simultaneously)
* add minor-rating
* show/hide "advanced" options (to reduce clutter)
* revisit forms to ensure validation is bullet-proof and help-text is complete and accurate
* better logging and easy access to it (presently if background tasks fail, logs are only accessible via an SSH session)
* better feedback in the UI when launching / stopping sessions
* better feedback in the UI when processing assets
* unify the ACSM UI and the Stracker UI
* REST API (to enable integration with in-game apps)

FAQs
----
Q: Can I contribute?
    A: Hell yeah!  Here's the source code: `ACServerManager`_

.. _ACServerManager: https://github.com/PeteTheAutomator/ACServerManager

Q: Any chance you can make the GUI a bit more... graphical?
    A: Yes.  Front-end development isn't my forte, but if I've learned anything in the 20+ years I've worked as a IT engineer is it's crucial to get your application's model correct.  The project is in early stages of development and I'm happy the model is solid - the framework I've chosen is extremely extensible so whizzy graphical stuff can be added later.

Q: What technology did you use?
    A: The code is written in Python, and there's a teensy bit of bash in there.  The web framework is Django.  I'm a Linux/Unix sys-admin so the server-side stuff is Linux and Python's a natural fit.

Q: Can I run more than one Session at a time?
    A: Presently NO - the web UI permits you to do that, but that won't work just yet.  The does model permit you to create multiple "Server Settings" - this is intentional, so provided define different sets of ports and only one Session Preset is launched with a particular Server Setting then YES - multiple sessions on a single server will be possible (at some point).

Contact
-------
peter.hehn@yahoo.com
