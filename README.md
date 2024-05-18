# CITS3403 Group Project

### Purpose

Sketchy is an interactive web application designed for collaborative drawing and guessing games. It allows users to create sketches based on randomised prompts and enables other users to guess the word or phrase represented by the sketch. The application's design focuses on facilitating user engagement and creativity.

Gameplay Experience:
- Sketchy offers an intuitive and user-friendly interface for creating sketches and guessing words or phrases represented by sketches.
- The gameplay flow is designed to be seamless, allowing users to switch between creating sketches and guessing sketches created by other users effortlessly.

Creative Expression:
- Sketchy provides users with a canvas and drawing tools to express their creativity and artistic abilities.
- Users can interpret given words or phrases in their unique style, resulting in a diverse range of sketches and interpretations.

Engagement:
- Leaderboards and scoring mechanisms encourage friendly competition and motivate users to improve their drawing and guessing skills.
- The guessing mechanism encourages users to interact with each other's sketches as the 'guesser' will be submitting their interpretations of the item.

### Group Members

| Name              | UWA ID   | Github        |
|-------------------|----------|---------------|
| Harry Ickeringill | 22986838 | @ickerio      |
| JJ Jun            | 22763977 | @jjwilliamjun |
| Henri Scaffidi    | 23245207 | @HenriScaff   |
| Ansu Regmi        | 23376904 | @ansuuuuuuu   |

### Architecture

The architecture of the Sketchy application follows a typical web application architecture, consisting of multiple layers and components that work together to provide the intended functionality.

The architecture of Sketchy is designed to be modular, scalable, and maintainable, allowing for future enhancements, optimizations, and feature additions. It emphasizes separation of concerns, adherence to best practices, and utilization of reliable technologies to deliver a robust and user-friendly drawing and guessing game platform.

Frontend Layer: The frontend layer of Sketchy comprises the user interface components visible to the users. It includes HTML, CSS, and JavaScript files responsible for rendering the application's pages, handling user interactions, and displaying dynamic content. Sketchy's frontend utilizes frameworks and libraries like Flask, Jinja2, Bootstrap, and jQuery to streamline development and enhance user experience.

Backend Layer: The backend layer handles the core logic and data processing of the application. It is implemented using Python with the Flask web framework. This layer includes routes, controllers, models, and services responsible for processing user requests, interacting with the database, and generating responses. Flask extensions such as Flask-SQLAlchemy, Flask-Migrate, Flask-Bcrypt, and Flask-Login are used to facilitate database operations, migration management, password hashing, and user authentication.

Database Layer: Sketchy utilizes a relational database to store application data. SQLAlchemy is used to interact with the database. The database schema includes tables for storing user information, sketches, words and guess sessions. SQLite is used for local development and testing.

Authentication and Authorization: Sketchy implements user authentication and authorization to control access to application features and data. Users can register accounts, log in securely, and access authenticated routes. Flask-Login is used for session management, while Flask-Bcrypt handles password hashing and verification to enhance security.

File Storage: ......

Testing Layer: Sketchy includes a testing layer for automated testing of application functionalities. -complete after all test incl

## Instructions

### Environment Variables

Before running the application, ensure you have set up the following environment variables:

- `SECRET_KEY`: A secret key for your application. This can be set in a `.env` file in the project root.

Example `.env` file:
```plaintext
SECRET_KEY=your-secret-key
```

### Launching

1. install python3 with `sudo apt-get install python3`
2. install pip with `sudo apt-get install python3-pip`
3. install venv with `sudo apt-get install python3-venv`
4. create new virtual environment with `python3 -m venv venv`
5. activate virtual environment with `source venv/bin/activate`
6. install requirements with `pip install -r requirements.txt`
7. run flask with `flask run`

## Testing

### Prerequisites
Before you begin, make sure you have completed the steps to set up and run the web application locally. Additionally, ensure you have the following Python packages installed:

- unittest

### Running Unit Tests

#### Step 1: Execute the Unit Tests
To run the unit tests, follow these steps:
1. Open your terminal or command prompt.
2. Navigate to the project directory.
3. Execute the following command:
```bash
python -m unittest unit_tests.py
```
#### Running Selenium Tests
#### Overview
In our application, we utilize Selenium for comprehensive end-to-end testing. Selenium is essential for automating browser tasks and testing complex user interactions within our web application.

#### Setup
Before running the Selenium tests, please ensure the following:

Selenium WebDriver is installed and configured correctly.
The specific WebDriver for your browser (e.g., ChromeDriver for Chrome, GeckoDriver for Firefox) is installed. 

```bash
python -m unittest selenium_unittests.py
```

### External Resources

 Images
- Logo: [Sketchy Logo]( )
- Favicon: [Favicon]( )

 JavaScript Libraries
- jQuery: [jQuery](https://code.jquery.com/jquery-3.5.1.min.js)
- Bootstrap: [Bootstrap](https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.bundle.min.js)

 CSS Files
- Bootstrap CSS: [Bootstrap CSS](https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css)

 Fonts
- Font Awesome: [Font Awesome](https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css)

