Workflow Thoughts
=================

Whilst it might make sense to reproduce the native windows server gui (so it's familiar to many) - that interface seems pretty awful.  As someone relative new to Assetto Corsa server management - these notes describe how I personally would approach the session configuration (workflow).


Steps
----- 

- deploy the server for the first time (superuser credentials will be set in ansible vars)
- upload fixtures to populate cars, tracks etc
- configure basic server settings (set a server name, welcome message, use default ports)
- configure a session preset:
  - environment:
    - select a track (choice of track dictates how many pitboxes are available, so this influences car selection)
    - weather
    - time of day
    - practice/quali/race
    - advanced (rarely touched - sensible defaults):
      - dynamism
      - realism
      - voting
  - cars:
    - pickup/booking?
    - organise by class
    - organise by brand
    - ad-hoc
  
