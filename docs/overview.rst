********
Overview
********
Before you jump into the Installation Guide it's worth getting an idea of what's involved.

Virtual Private Server
----------------------
This project's server component is built to run on Linux (RedHat7 or CentOS7) - the easiest (and cheapest) option is to
use Amazon Web Services (AWS) and take advantage of their **free tier** offer on the smaller EC2 Instances (Virtual
Private Server).  **Free tier** means you can run a 1 CPU, 1GB RAM, 8GB storage server instance **FREE-OF-CHARGE** for your
first year of membership with AWS - the spec of this machine is more than enough to run the Assetto Corsa server with
24+ users racing.  To sign-up as an AWS customer you will need to provide billing information as the service charges for
your hourly usage - even though this should be zero (you can check your bill to the latest hour at any time).  AWS has
datacentres located in several regions around the world so to optimise network performance it's best to run your server
in a region physically close to you and your racing partners.  Personally I live in central England and I run my server
in Ireland - my ping is around 22ms.

Assetto Corsa Software
----------------------
You will need the PC version of the Assetto Corsa game, and also have installed the "Assetto Corsa Dedicated Server"
software on your PC.  The Assetto Corsa Dedicated Server software is free-of-charge as an optional component so long
as you have the game (in Steam you can find this under the "Tools" section).  Although your PC won't be running the
Dedicated Server program it's necessary to have this available so that it can be copied to your server.  Certain assets
such as car and track metadata also need to be copied from your PC to the server - don't worry; I've written a tool
(called **assetOmator**) that will handle that business for you.  This also means if you decide to with a car or on a track
that you've sourced from the Assetto Corsa modding community which you've installed on your PC, the **assetOmator** can
sync those mods to your server for you.

Additional PC Software
----------------------
In order to sync Assetto Corsa software from your PC to your server you will need to run the **assetOmator** tool on your
PC which I've written using the Python language - this isn't native to Windows so you'll probably need to grab it (don't
worry - it's free).  Once you have Python installed it's a quick step to install **assetOmator** - I'll cover those
details in the Installation Guide.
