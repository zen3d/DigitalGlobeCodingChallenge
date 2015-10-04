# Digital Globe Coding Challenge

This project is my solution to the Digital Globe coding challenge.

The elements of the coding challenge are:
  * Create a URL shortening service
  * Put it behind a cherrypy Rest API in a meaningful way
  * The service must be built as a Docker image
  * Put the code in Github in a way that makes sense: Readme file, etc  	
  * Make it pretty as if someone's going to use it
  * Deploy to a cloud provider of your choice
  * Rate limit the service to 2 requests per second
  * Bonus: for any kind of GUI 

This repo contains the files that solve this challenge:
  * webapp/server.py
  * Dockerfile

server.py is a Python file that uses cherrypi to create a REST server. 

The three main methods in the Root object are:
  * index - handle accesses to /, permitting the requester to enter a URL to be shortened
  * new_url - show the shortened URL that was created for the requester of the service and it's shortened abbreviation
  * default - handle shortened abbreviations and redirect to the URL requested
  
A utility function is also provided (hash_str) that takes a string containing the URL to be abbreviated, hashes it, and returns a 6 character string corresponding to that URL string.

Dockerfile contains the settings and initialization for the docker container. It initializes the container to contain a resonable set of Python packages, including the essential cherrypy package.

To build the Dockerfile, do:
 docker build -t <my_docker_ID>/mywebapp:latest .

To run the Dockerfile, do:
 docker run -p 80:8080 -i -t <my_docker_ID>/mywebapp:latest
 
Replace <my_dicker_ID> with your personal docker ID.
