# The Cocktail Codex

#### Video Demo:  https://youtu.be/NEvA0XV-UEI

#### Description:
## app.py
### register
This route contains code to register a new user. It asks for their name, email address, username, password, and password confirmation. It will check that the user has completed all the fields, that the password and password confirmation match, and that the username is not already taken. If any of these conditions fail, an error message will be generated. It will then hash the password to store in the users table in cocktails.db. when a user registers, they will automatically be added to the bars table with their user id and bar name (which defaults to "Name's Bar" where name is the name the user enters during registration).
### login
This route contains code to log a user in taken from the CS50 Finance problem in pset9. It checks that the user completed both fields (username and password). It will then check the password hash against the password in the users table and check that there is a row for that username and password combo. If there is no row, then the username and/or password is invalid or doesn't exist and an error message will be displayed.
### logout
This route contains code to "forget" the user that was logged in. It clears the session.
### settings
This route contains code to allow the user to change their username, email address, and/or password in the database. If a field is blank (for example, they don't type in a new username), then that field will not be updated in the users table. If they want to change their username, the code will again check that the username doesn't already exist. If they want to change their password, they must first enter their current password which will be hashed and checked against the password for that username in the users table. The code will also check that the new password matches the new password confirmation. If the user does enter text to change a field (i.e. username), that column will be updated in the users table to reflect the change.
### forgot
This route contains code for if the user forgets their password. I was not able to setup email in flask for this program, so if the user clicks forgot password they will just be redirected to a page where they must enter their username, email address, and new password. If the username and email address match the user in the users table then they will be allowed to choose a new password. Ideally, I would have liked to have a forgot password link sent to the user's email, but was unable to get this to work for this program.
### mybar
This route is the first one the user should interact with once they create an account. It will display the option to update their bar, view the ingredients they have, view their favorite recipes, or view the recipes they are able to make. It just contains links to other pages on the website. The one variable that must be passed through is the bar name from the bars table in cocktails.db because it will be displayed on the page.
### myingredients
This route will display the ingredients the current user has added to their bar. It will go into the bars table and display all of the ingredients where the user id matches that of the current user.
### update
The user can click "Update Bar" and will be taken to this page. This will allow them to change the name of their bar and add or remove ingredients. "Remove Ingredients" will only display ingredients that are already in the bar of that user (in the bars table). "Add Ingredients" will only display ingredients that are NOT already in the bar of that user. When the user clicks save, any ingredients checked under Remove will be deleted from the bar table where the user id is equal to that of the current user and the id is equal to the id of that specific item. . Any ingredients checked under Add will be inserted. And if the bar name is blank, nothing will update but if a new bar name is entered, the "bar name" column will be updated for every row that matches the current user's user id.
### favorites
If this route is reached via GET, it will just display all of the recipes the user has favorited by going into the favorites table and displaying all of the ones where the user id matches that of the current user. If this route is reached via POST, it allows the user to add a new recipe to their favorites. When the user clicks "+ Add to Favorites" it will first create a list of all the recipes already in favorites. If the new recipe is not in favorites, it will be added and the user will be taken back to the recipes page. If it is already in favorites, the user will see "Favorited. View your favorites." and then the route will take the user to their favorites page.
### available
This route displays the drinks the user is able to make based off the ingredients they have added to their bar. It will create a list of all the possible drinks, then create a list of all the ingredients the user has on hand. It will then go through each drink using a loop and create a list of ingredients for that particular drink. It will then user another loop to go through each ingredient in the drink and check if it is in the list of ingredients the user has on hand. If it is in the list, it moves on to the next one. If it is not in the list, it adds 1 to the count. At the end of the loop, the code will check the count. If the count is still 0, that drink gets added to the list of available drinks. If the count is 1, it gets added to the list of "missing1", meaning the user is missing 1 ingredient. This goes on up to "missingmore", which means the user is missing 4 or more ingredients for that drink.
### drinks
This route just displays a list of all the drinks in the database and allows the user to view the recipe of a drink.
### ingredients
This route displays a list of all the ingredients in the database and allows the user to search for recipes by the ingredient.
### recipe
The user arrives to this route after clicking on the name of a recipe anywhere on the site. It will first get the name of the drink and then check if that drink is in the database already. If it is not, it takes the user to a page to add a recipe. If it is, it will create a variable called RECIPES that includes all of the ingredients and quantities where drink=drink. It will then create a variable called INSTRUCTIONS that groups by instructions so the instructions are only displayed once. This route also checks the ingredients the user has compared to the ingredients in the recipe and will add the name of the ingredient to a list of missing ingredients if the recipe calls for an ingredient that the user does not have. Last, it will check if the drink is already favorited and display a different message if it is or isn't favorited.
### add1 and add2
These routes are basically the same. The only thing that changes is if the user reaches it from clicking "Add ingredient" then it renders a template where a text box will display for the user to type in the ingredient name and if the user reaches it from being redirected while adding a new recipe, the ingredient name will automatically be displayed. Either way, this route will check that the user has entered an ingredient and type and then insert the ingredient and type into the ingredients table.

## cocktails.db
### users table
This table contains the information of all the registered users including: id, username, hash(password hash), name, email, and bar name (default's to "Name's Bar" including the person's name).
### recipes table
This table contains recipe id, drink name, ingredient, quantity of that ingredient, and instructions. The drink name and instructions will be repeated in every row of ingredients/quantities for that recipe.
### ingredients table
This table contains ingredient id, ingredient name, and ingredient type.
### bars table
This table contains information about the users' bars. It includes the row id, user id, bar name, and ingredients that particular user has added to their bar.
### favorites table
This table contains the favorites of each user. It has a user id and drink name column.

## helpers.py
This file just contains the code for login required from CS50x Finance in pset9.

## templates
### add.html
The template for adding a recipe. Includes javascript to allow the user to add additional ingredients as needed. When add ingredient is clicked, additional text boxes will appear for quantity and ingredient.
### addingredient.html
This template is for when the user clicks on "Add ingredient" somewhere on the site. It will display a text box for ingredient name to be typed in and a dropdown of ingredient types.
### addredirect.html
This template is similar to the above, but will appear if the user types an ingredient in while adding a recipe and that ingredient is not yet in the databse. The ingredient name will already appear and the user will just have to select the ingredient type from the dropdown.
### available.html
Includes collapsible content boxes to show what recipes fall into each category (missing 0 ingredients, missing 1, missing 2, etc). I chose to do collapsible content boxes for this so the page didn't seem overwhelming, especially if the user is only interested in what drinks they can make. They can choose which categories they actually want to view.
### drinks.html
Allows the user to select a drink either by browsing all recipes in alphabetical order or typing into a search box that will autocomplete from the datalist.
### drinks2.html
A slightly altered version of drinks.html. The user will be taken to this page if they are viewing recipes by ingredient and it will display the ingredient name on the page. It will only display recipes that can be made with that particular ingredient.
### favorites.html
This template displays the user's favorited recipes.
### forgot.html
This template includes text boxes for the user to enter username, email, and password.
### index.html
This template just displays "Welcome to "Bar Name"".
### ingredients.html
Allows the user to select an ingredient either by browsing all ingredients by type in alphabetical order or typing into a search box that will autocomplete from the datalist.
### layout.html
This file includes the code for the header image, navigation bar, and footer for the entire site. It is carried over to other files via Jinja code.
### login.html
This template includes text boxes for the user's username and password. It also includes a link to register if the person doesn't have an account yet.
### mybar.html
This template includes links to update the user's bar, view ingredients, view favorite recipes, or view available recipes.
### myingredients.html
Similar to the ingredients.html page, but this page will only display the ingredients this user has in their bar.
### recipe.html
This page will display a recipe.
### register.html
This page will display text boxes for the user to enter their name, email, username, and password. It also includes a link to login if the user already has an account.
### settings.html
This page displays text boxes with headers to allow the user to enter a new username, email, or password.
### update.html
This page is divided into 3 collapsible content boxes, again so the user isn't overwhelmed by a long page full of items they may not need at the moment. The first collapsible is to rename their bar, the second is to remove ingredients from their bar, and the third is to add ingredients to their bar. There is also a link to add an ingredient if they want an ingredient that isn't listed.

## static
### styles.css
This file contains all of the css for the entire site. Most of it affects links and buttons.


Certainly! Here's the README written in markdown format:

## The Cocktail Codex

### Introduction
The Cocktail Codex is a web application that allows users to register, create their own bar, manage ingredients, browse recipes, and discover cocktails they can make based on their available ingredients. The application aims to simplify the process of exploring and experimenting with cocktail recipes. With a user-friendly interface and robust functionality, The Cocktail Codex provides an enjoyable experience for cocktail enthusiasts.

### Installation
To run The Cocktail Codex locally, follow these steps:

1. Clone the repository from GitHub:
   git clone https://github.com/your-username/cocktail-codex.git

2. Navigate to the project directory:
   cd cocktail-codex

3. Install the required dependencies:
   pip install -r requirements.txt

4. Set up the database:
   - Create a new database using a database management tool of your choice.
   - Import the `cocktails.db` file into your database.
   - Update the database connection settings in the `config.py` file.

5. Start the application:
   ```
   python app.py
   ```

6. Access the application in your web browser at `http://localhost:5000`.

### Usage
Once the application is running, you can perform the following actions:

- Register a new user account by providing the required information.
- Log in using your username and password.
- Customize your bar by adding and removing ingredients.
- Browse the list of available cocktails based on your bar's ingredients.
- Explore and view detailed recipes for various cocktails.
- Favorite recipes to access them easily in the future.

### File Structure
The project follows the following file structure:

```
cocktail-codex/
├── app.py
├── config.py
├── cocktails.db
├── helpers.py
├── requirements.txt
├── static/
│   └── styles.css
└── templates/
    ├── add.html
    ├── addingredient.html
    ├── addredirect.html
    ├── available.html
    ├── drinks.html
    ├── drinks2.html
    ├── favorites.html
    ├── forgot.html
    ├── index.html
    ├── ingredients.html
    ├── layout.html
    ├── login.html
    ├── mybar.html
    ├── myingredients.html
    ├── recipe.html
    └── register.html
```

### Configuration
The Cocktail Codex requires the following configuration:

- Database settings: Update the database connection settings in the `config.py` file to match your database configuration.

### Deployment
To deploy The Cocktail Codex to a server or hosting platform, follow the standard procedures for deploying a Flask web application. Ensure that you have the necessary server environment and database setup. Then, deploy the application code to your server and configure the server settings accordingly.

### Contributing
Contributions to The Cocktail Codex are welcome! If you would like to contribute, please follow these guidelines:

- Report any issues or bugs by creating a new issue on the GitHub repository.
- Suggest improvements or new features by creating a new issue on the GitHub repository.
- Submit pull requests with your proposed changes, ensuring that they adhere to the project's coding style and guidelines.

### License
The Cocktail Codex is currently not licensed.

Please note that this project is provided as-is, without any warranty or guarantee.