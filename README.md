# CITS3403 Group Project

### Purpose

TODO a description of the purpose of the application, explaining the its design and use.

### Group Members

| Name              | UWA ID   | Github        |
|-------------------|----------|---------------|
| Harry Ickeringill | 22986838 | @ickerio      |
| JJ Jun            | 22763977 | @jjwilliamjun |
| Henri Scaffidi    | 23245207 | @HenriScaff   |
| Ansu Regmi        | 23376904 | @ansuuuuuuu   |

### Architecture

TODO a brief summary of the architecture of the application.

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

