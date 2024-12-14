This is my readme file! Read-me and weep.

Overview
This project scrapes the Shepherd catalog, and displays it on a website.
The "data_maker" submodule is what scrapes the data. There should probably be a separate website and scrape module...


# Important
If you want to run as a package, you need to have the templates and static folder in the working directory, or in a subdirectory.
The webserver will search every folder in the working directory until it finds the "templates" and "static" folder.

Meaning, you will have to download the project from github, and run the package while inside the project folder.

Which really defeats the whole point of having it be a package... So you could just download the static and templates folder too.
But I spent like an hour trying to make it not like this and I couldn't figure it out.

Besides that, tnstalling one of the packages and doing 
python -m shepherd_course_picker
makes it go. the webiste will be at http://localhost:5000 (it will also say this in the terminal window you run it in)


Usage:

The landing page of the website has a list of programs.
Pick one and click on it to move to the 2nd page.

The 2nd page has an overview of the course on the left, and a "shopping cart" of courses on the right.
Clicking on a course, be it on the left or right, will toggle rather it is in the cart or not.
The total amount of credits in your cart is displayed at the top of the cart.

That's all it does!


Stupid things:
OR condition courses don't work on the JS side of things. It is represented perfectly within data structure though.
Tables are not implemented on the website. There *should* be text saying "Table not implemented".
Some nodes will have a parent node with nothing but themselves in it.


Errors you will encounter:
Any error on the website should bring you back to the Program selection page after clicking "OK".
A mysterious error like
    "Something: "Error: 'NoneType' object has no attribute 'find_all'""
is because the scraper module failed to scrape the selected program.