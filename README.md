# Job finder tool 

## Overview

This project is an excuse for me to learn the selenium for python module and the django framework, therefore it is slow by design as it's not for example using the indeed API which would be quicker.
The goal of this project is not for a fast site.

This project is a local website made using the django framework alongside some static html, css, and javascript in order to have a nice interface for running a selenium script.
The website is designed to take user details once, and find theoretically all available jobs instead of typing the same details in all different job sites.

The core of this project is very basic, the user inputs their details into a html form which then calls the selenium script, returns the search results and creates a new html page based of that, that's it. I used django to connect the two and django's inheritance features to make this simpler and more scalable in the future if I decide to do more with this project.
### Main goal:

- A local website that has links to appropriate jobs held on online job boards


### Screenshots:
Home page:

![Image of the home page for this project](docs/assets/home.png)

Result page:

![Image of the result page given a user search](docs/assets/result.png)
### Future possibilities:

- show hourly rate
- default to not showing previously applied jobs
- label for each link for how easy it is to apply i.e.
    - 1 = very simple, has "apply now" button
    - 2 = must apply on company website
    - 3 = call company
- automate the application for the jobs found
