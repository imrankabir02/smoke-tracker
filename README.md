# Smoke Tracker

Smoke Tracker is a web application designed to help users monitor and reduce their smoking habits. It provides tools for logging smokes, setting daily goals, and analyzing smoking patterns to support users in their journey to quit.

## Live Demo

[Link to Live Demo](#)

## Features

- **User Authentication:** Secure user registration and login.
- **Setup Wizard:** A guided process for new users to set up their profile, daily goals, and preferred brands.
- **Dashboard:** A central hub displaying key metrics like time since last smoke, daily progress, and cost analysis.
- **Smoke Logging:** Users can log each smoke with details such as brand, trigger, and mood.
- **Quick Log:** A one-click option to log a smoke using predefined defaults.
- **Detailed Statistics:** Comprehensive analytics with charts on smoking frequency, triggers, mood changes, and cost.
- **Brand Management:** Users can add, edit, and delete their preferred cigarette brands and associated prices.
- **Goal Setting:** Set and update daily smoking limits to encourage reduction.
- **User Profile:** Manage account settings, including timezone, currency, and password.
- **Admin Dashboard:** An admin-only section to view site-wide statistics and manage user-submitted brand requests.

## Technologies Used

- **Backend:** Django, Python
- **Frontend:** HTML, CSS, JavaScript, Bootstrap 5
- **Database:** SQLite (default), compatible with PostgreSQL, MySQL
- **Libraries:**
  - `django-crispy-forms` for form rendering.
  - `crispy-bootstrap5` for Bootstrap 5 integration.
  - `pytz` for timezone handling.

## Setup and Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/imrankabir02/smoke-tracker.git
   cd smoke-tracker
   ```

2. **Create a virtual environment and activate it:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: A `requirements.txt` file will be created in the next step.)*

4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

## Usage

After setup, navigate to `http://127.0.0.1:8000/` in your browser. You can sign up for a new account or log in as the superuser to access the admin dashboard.

## Project Structure

```
smoke-tracker/
├── smoketracker/         # Project-level configuration
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── tracker/              # Main application
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   ├── middleware.py
│   ├── templates/
│   └── ...
├── static/               # Static files (CSS, JS)
├── templates/            # Base templates
└── manage.py
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature-name`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
