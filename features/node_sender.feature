Feature: Get Echo Message
 Send message and get echo response
 User that send message
 Get echo response
 To check server

    Scenario: turn on server
        Given a docker client
        When two servers is not live
        Then turn on two server

    Scenario: send a message to server
        Given two server
        When two server is on
        Then issue a message to echo server
        Then get a message
  
 