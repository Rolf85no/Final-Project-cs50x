# MY RECIPES

#### Video Demo:  <https://youtu.be/hlUTidbIuZE>

#### Description:
This is a web-application where the user can save recipes from other websites, she can also see recipes that other users have uploaded.
The user can either copy/paste the recipe name, recipe, link to website and link to picture or write it in manually. I prefer to copy/paste.
I have used Python, SQL, JavasScript and Jinja.
The reason I made the website is that I use a lot of online recipes and find it annoying to have to scroll through a lot of text to get to the recipe.
Some website for example tell a long story about how they discovered the recipe, the first time they ate it and so forth.
There is also the annoyance of pop-up auto play video windows, and ads.
So this is a website where the user can store there favourite recipes and just keep the information they need.
The recipe text is formatted so all recipes look the same on the My Recipes website.
All the info is stored in a database file using Python and shown on the html.page using Jinja.

I have used boostrap for the layout on all html pages, in addittion to my own css.
All html-pages extends layout.html.
For all messages, like "invalid password", "logged in", "uploaded recipe" etc I have used the get flashed message function.
I chose the closest color I could get to the rest of the site which was the success color.

#### application.py:
This is where I run the app, I used pset9 finance as a starting point.
Here I query the database, store the queries in variables and pass them to the different html-pages,
I also store and format the text that is beeing stored from the upload.html page to the database.
I used a login form where i hash the password using werkzeug.security check_password_hash function and check that it matches the hashed password in the database.
On the "/" and "/all" route I use get to show all the recipes, and post to filter the different meal types that are stored in the database.

On the "/upload" route I format the recipe text using re, to remove unwanted symbols. For example a lot of recipes have a checbox next to the ingredients.
I also make sure that each line has no more than 48 words and remove unwanted space before and after text using text_wrap.
All the names of the recipes are capitalized.

On the "/inspiration" route I return a html-site where I hard-coded some websites and descriptions in the html.

#### helpers.py
This contains the same login_requiered function as in Pset9 finance, and is imported in application.py

#### recipes.db

Here i have two tables, users and recipes. The users table stores user_id password and name.
The recipes store recipe name, recipe text, website, link to a photo of the recipe, user_id and tags for the different recipes.
I have used the primary key of users as a foreign key in recipes and saved it as recipes_user.

#### index.html and all.html

In index.html the user sees all the recipes she has stored.
I have used bootstrap borderless tables as a framework. At first I had the borders but it looked at bit too formal and stiff for me.
By having a borderless table it resembled a menu in a way that i liked. Especially with the picture on the same line as the name of the recipe.
Using a Jinja for loop I show all the different recipe tags stored in the database of the user in a dropdown menu where the user can filter the different meal-types.
I have used another Jinja for loop to show the name of recipe, tag, recipe text and picture of meal in a table.
For the recipe text I have used a collapse button to save space. That was one of the first ideas I had.
It would just get too cluttered if the user couldn`t hide the recipe text.

At first I just had a green navbar, but it looked a bit boring so I changed to a picture of some vegetables.
The colors on all the buttons and the header is the same shade of green as on the picture. At least according to: https://imagecolorpicker.com/

I went back and forth a lot on how many different colors there should be on the text elements. I tried different colors that complimented
that exact green color. In the end i landed on green, white and black because it can start to feel very homepage in the 90s with too many colors.
If feel most webpages now adays is very clean.

All.html has almost the same functionality and code as index. The only differences is that here it shows the recipes that all users have uploaded.

#### inspiration.html

Here I have hard-coded some websites and descriptions.

#### login.html

This is just a simple form to get the username and password.
In application.py I store the username and password in variables and check if they exist in the database.
If not it flashes "Invalid username and/or password"
This is exactly the same as I used in pset9.
When logged in it flashes logged in.

#### layout.html
This is copy/pasted and tweaked from pset9. I removed the icon, and changed the color of the text, changed the background of the navbar,
and number of links in the navbar.


#### register.html
In application.py I store the username and password in variables and check if they are not in the database,
if password and confirmation match or if they are blank.
If any error or when registered an appropriate flash message is shown.

#### upload.html
This page has a form where the user can upload all the variables that will be stored in the database.
For the form column where the recipe text is placed I have used a Javascript function to make sure that you can press enter to write a new line instead of the form begin submitted.
This makes it easier to edit the text. It`s a tweaked version of a Javascript I found that was used to make a message chat box.
I have also used css to define the size of the text-box.

In the picture link field I have included an explanation on how to copy the picture-link.
That was after a request from my girlfriend, who didn`t know how to do it.
The last field is an dropdown menu too chose type of meal.
The types are pre-defined in a python-list.
At first I had a text-field, but it would be too chaotic because users could misspell or define food in so many different ways making the filter function a bit useless.

#### script.js

I could have just included it in the html but I wanted to try an use it in an external file so I could learn how to do it.
As mentioned in upload.html. The script make sure the user can press enter without submitting the form.

#### styles.css

I made the toggler a bit more visible when collapsing the navbar.
It became almost invisble when I changed from a green navbar to a navbar with a background image.
I just made the background-color the same green color as on the photo but with opacity at 0,6 and made a black border.

Using bootstrap for styling has been both really annoying and useful. It took me a long time too figure out I had to write important to change for example
the color of the links on the navbar when hovered. I think what I spent a lot of time tweaking the bootstrap css,plus the html css in general.
The layout is not super inspired. It works. I have to admit there is a lot of trial and error here.
I have created som classes to for example center the text instead of having it on the left,
underlining links but not making them blue when hovering.
Im happy with the use of the pre tag and how I added attributes to the css to keep the formatting from application.py but adjusting it to the website.
Maybe some of the css is redundant but I just got so tired of fighting it, so I made a choice to focus more on functionality than design.
On my next webpage I will try to not use boostrap in order to understand a bit more of the css and html.

