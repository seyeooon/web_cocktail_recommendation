
# Cocktail Recommendation Website

This project is a Django-based web application that provides cocktail information and personalized recommendations based on user preferences. The website also features community functions and a search feature for exploring a wide range of cocktails.

## Features

- **Main Page**: Displays a dynamic grid of cocktail recommendations categorized by spirits, alcohol strength (proof), and techniques.
- **Cocktail Detail Page**: Each cocktail has detailed information on ingredients, preparation method, alternative ingredient suggestions, and related music recommendations.
- **Personalized Recommendations**: Registered users can save their preferences and receive personalized cocktail recommendations based on those settings.
- **Search Functionality**: Users can search for cocktails by name or ingredients.
- **Community Page**: Includes both general community discussion and cocktail-specific community pages for users to share their experiences.
- **User Authentication**: Users can log in, register, and save personalized preferences on their "My Page."

## Installation

### Prerequisites

- Python 3.12.7
- Django 3.x
- Virtual environment (recommended)

### Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/seyeooon/web_cocktail_recommendation.git
   cd web_cocktail_recommendation
   ```

2. **Create a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scriptsctivate
   ```

3. **Install Required Packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Database Migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the Website**: Open your browser and go to `http://127.0.0.1:8000`.

## Project Structure

- `web_cocktail/`: Contains project settings, URLs, and ASGI/WSGI configurations.
- `main/`: The main application for the homepage and user interactions.
- `cocktail/`: Manages cocktail information, details, and search functionality.
- `community/`: Handles both general and cocktail-specific community pages.
- `login/`: Manages user authentication and session handling.
- `search/`: Implements the search functionality for cocktails.
- `static/`: Each app has its own folder for static assets (CSS, JavaScript, images).
- `cocktail_data.json`: JSON file containing the cocktail data used throughout the website.

## Key Files

- `manage.py`: The main script for running Django commands.
- `db.sqlite3`: SQLite database used for local development.
- `cocktail_data.json`: JSON file that contains detailed information about cocktails (ingredients, preparation methods, etc.).

## Usage

1. **Register/Login**: Users can create an account or log in to access personalized recommendations.
2. **Browse Cocktails**: Explore different cocktail categories or search for specific cocktails.
3. **Join the Community**: Participate in discussions on cocktail-specific or general community pages.
4. **Set Preferences**: Customize your preferences on "My Page" to receive personalized recommendations.

## License

This project is licensed under the MIT License.
