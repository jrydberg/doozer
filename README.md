# Doozer

Another very simple build server using Docker.

The problems it tries to solve:

* build your software in a reproducable manner
* test your software in a reproducable manner
* help your deploy your software in a reproducate manner
* provide a usable API

The problems it does not try to solve:

* manage artifacts, there are better tools for that
* report on stuff like code coverage, there are better tools for that
* having N slaves connected and spread builds over those
* access control and user management

What it targets:

* GitHub or GitHub Enterprise as identity for both code and users

