# The Cocktail Codex

### Introduction
The Cocktail Codex is a web application that allows users to register, create their own bar, manage ingredients, browse recipes, and discover cocktails they can make based on their available ingredients. The application aims to simplify the process of exploring and experimenting with cocktail recipes. With a user-friendly interface and robust functionality, The Cocktail Codex provides an enjoyable experience for cocktail enthusiasts. This project was created as the final project for CS50X.

### Installation
To run The Cocktail Codex locally, follow these steps:

1. Clone the repository from GitHub:
   ```
   git clone https://github.com/your-username/cocktail-codex.git
   ```

2. Navigate to the project directory:
   ```
   cd cocktail-codex
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

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

### License
The Cocktail Codex is currently not licensed.

Please note that this project is provided as-is, without any warranty or guarantee.

Contact me about this project at ginacostanzo13@gmail.com