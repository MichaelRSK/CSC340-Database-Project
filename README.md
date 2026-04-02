# Store Manager GUI (Activity 4)

Python + Tkinter + MySQL application with login, role-based dashboards (`owner`, `manager`, `employee`), account creation, username autocomplete, and inactivity timeout.

## Requirements

- Python 3.10+
- MySQL Server
- Windows PowerShell (commands below assume PowerShell)

## Setup

1. Open PowerShell at the project root:
   - `C:\Users\Michael\CSC 340 Database\CSC340-Database-Project`
2. Create and activate virtual environment:
   - `python -m venv .venv`
   - `.\.venv\Scripts\Activate.ps1`
3. Install dependencies:
   - `pip install -r requirements.txt`
4. Create local env file:
   - `copy .env.example .env`
5. Edit `.env` with your DB credentials:
   - `DB_HOST=localhost`
   - `DB_PORT=3306`
   - `DB_USER=root`
   - `DB_PASSWORD=your_mysql_password`
   - `DB_NAME=store_db`

## Database Setup

1. Open MySQL:
   - `mysql -u root -p`
2. Run:
   - `source sql/schema.sql;`
3. Exit MySQL:
   - `exit`

`schema.sql` now handles both:
- fresh database setup
- existing databases that need the `owner` role added

## Run the GUI

- `python -m store_app.main`

The app always opens at the login screen.

## Default Account Behavior

- On startup, manager seed runs unless disabled by env:
  - `SEED_MANAGER_ON_START=true`
- Seed credentials come from `.env`:
  - `SEED_MANAGER_USERNAME`
  - `SEED_MANAGER_PASSWORD`

## Creating Accounts

- `manager` and `owner` can create users from the dashboard (`Create User` button).
- `manager` can create: `employee`, `manager`
- `owner` can create: `employee`, `manager`, `owner`
- `employee` cannot create users

## Login and Roles

- `owner` -> owner dashboard
- `manager` -> manager dashboard
- `employee` -> employee dashboard

Each role sees different navigation options.

## Inactivity Timeout

- Activity (mouse/keyboard) resets timer.
- On timeout, a warning popup appears with a 60-second countdown.
- If still inactive after countdown, user is logged out and returned to login.

## Troubleshooting

- **PowerShell redirection error with `<`**
  - Use MySQL `source` command instead of shell redirection.
- **Access denied for MySQL user**
  - Check `.env` credentials (`DB_USER`, `DB_PASSWORD`).
- **`mysql` command not found**
  - Add MySQL `bin` folder to PATH or open MySQL Shell directly.
