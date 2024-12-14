# Overview
This project scrapes the Shepherd catalog, and displays it on a website.  
The "data_maker" module is what scrapes the data. "webapp" module contains the webapp.

The data_maker works perfectly fine on its own without the webapp portion.


# Monkey Business
<strong>To run as a package, you need to have some project folders in the working directory, or in a subdirectory. </strong>
The files it needs are CSS, JS, and HTML. Meaning I can't just simply import them.
The Flask app will search every folder in the working directory until it finds the "templates" and "static" folder.

Meaning, you will have to download the project from Github, and run the package while inside the project folder.

Which really defeats the whole point of having it be a package... But you *could* download just these two required folders.

I spent over an hour trying to make it not like this and I couldn't figure it out.
## Example of what I mean
1. Download the project from Github
2. Unzip project.zip
3. cd /project
4. python -m shepherd_course_picker

# Usage
1. Just installing the package and doing
   python -m shepherd_course_picker  
   Will make it go.
   The website will be at http://localhost:5000 (it will also say this in the terminal window you run it in)

2. The landing page of the website has a list of programs.  
   Click on one to move to the next page

3. This page has an overview of the course on the left, and a "shopping cart" of courses on the right.  
   Clicking on a course, be it on the left or right, will toggle it in and out of the cart.

- The total amount of credits in your cart is displayed at the top of the cart.

That's all it does!


# Stupid things
- OR condition courses don't work on the JS side of things. It is represented perfectly within data structure though.
- Tables are not implemented on the website. There *should* be text saying "Table not implemented".
- Some nodes will have a parent node with nothing but themselves in it.


# Errors you will encounter
- Any error on the website should bring you back to the Program selection page after clicking "OK".
- A mysterious error like  
  "Something: "Error: 'NoneType' object has no attribute 'find_all'""  
  is because the scraper module failed to scrape the selected program.
  I know the 2nd program does this
