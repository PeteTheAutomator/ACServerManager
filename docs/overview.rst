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
24+ users racing.

Full details can be found at this page: `Amazon Free Tier`_

.. _Amazon Free Tier: https://aws.amazon.com/free

To sign-up as an AWS customer you will need to provide billing information as the service charges for
your hourly usage - even though this should be zero (you can check your bill to the latest hour at any time).  AWS has
datacentres located in several regions around the world so to optimise network performance it's best to run your server
in a region physically close to you and your racing partners.  Personally I live in central England and I run my server
in Ireland - my ping is around 22ms.

Assetto Corsa Software
----------------------
You will need the PC version of the Assetto Corsa game, and also have installed the "Assetto Corsa Dedicated Server"
software on your PC.  The Assetto Corsa Dedicated Server software is free-of-charge as an optional component so long
as you have the game (in Steam you can find this under the "Tools" section).  Although your PC won't be running the
Dedicated Server program it's necessary to have this available so that it can be copied to your server.

Additional PC Software
----------------------
In order to sync Assetto Corsa software from your PC to your server you will need to install and run the **assetOmator** tool
on your PC which I've written using the Python language - Python isn't native to Windows so you'll need to install it
(don't worry - it's free).  Full details are covered in the Installation Guide.
