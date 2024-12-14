This is my readme file! Read-me and weep.

Overview
This project scrapes the Shepherd catalog, and displays it on a website.
The "data_maker" submodule is what scrapes the data. There should probably be a separate website and scrape module...


Using this:


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