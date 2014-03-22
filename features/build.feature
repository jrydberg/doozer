Feature: building software
  In order to test and deploy software it needs to be built

  As a developer
  I want my code to be built
  So I can test and deploy it

  Scenario: Failing build
    Given a manifest with build step "/bin/false"
     When I build my software
     Then doozer exits with exit code 1

  Scenario: Successful build
    Given a manifest with build step "/bin/true"
     When I build my software
     Then doozer exits with exit code 0
