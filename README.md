# Gas Utility Service Project

This project is a Django-based web application for managing gas utility customer services, including account management, service requests, and administrative operations.

## Project Structure

- `gas_utility_service/` - Main Django project directory
  - `accounts/` - Handles user accounts and authentication
  - `customer_service/` - Manages customer service requests and service types
  - `gas_utility/` - Django project settings and configuration
  - `templates/`, `static/`, `media/` - Frontend assets and uploaded files
  - `manage.py` - Django management script
  - `run.sh` - Shell script to set up and run the server
- `attached_assets/` - (Optional) Additional project assets
- `pyproject.toml`, `uv.lock` - Python dependencies and lock file

## Requirements

- Python 3.11+
- Django 5.1.7+
- (Recommended) Virtual environment tool (e.g., venv, virtualenv)

## Setup Instructions

1. **Install dependencies**

   From the `BuildAndRun` directory:

   ```bash
   pip install -r requirements.txt
   # or, if using pyproject.toml/uv:
   pip install django>=5.1.7
   ```

2. **Run the application**

   Use the provided shell script to set up the database, create initial data, and start the server:

   ```bash
   cd gas_utility_service
   bash run.sh
   ```

   This will:
   - Apply database migrations
   - Create a default admin user (`admin` / `admin`)
   - Populate service types
   - Start the Django development server at [http://0.0.0.0:5000/](http://0.0.0.0:5000/)

3. **Access the application**

   - Visit [http://localhost:5000/](http://localhost:5000/) in your browser.
   - Admin interface: [http://localhost:5000/admin/](http://localhost:5000/admin/) (login: `admin` / `admin`)

## Notes

- Media uploads are stored in `media/request_attachments/`.
- Default database is SQLite (`db.sqlite3`).
- For production, update `DEBUG`, `ALLOWED_HOSTS`, and database settings in `gas_utility/settings.py`.

## License

This project is for educational/demo purposes. 