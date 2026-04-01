# Activity 4 — TODO List
**Store Manager GUI | Michael Krueger & Creed McFall**

> Tasks are ordered by dependency — complete them top to bottom.
> Each task is tagged with a suggested assignee. Split however works best for your group.

---

## Phase 1 — Project Setup
*Do this together before splitting work*

- [ ] Create GitHub repository for Activity 4
- [ ] Add Creed as collaborator
- [ ] Add instructor as collaborator (GitHub: `rkandru`)
- [ ] Set up project folder structure (see below)
- [ ] Create and activate a Python virtual environment
- [ ] Install dependencies: `pip install mysql-connector-python pillow`
- [ ] Create `requirements.txt` (`pip freeze > requirements.txt`)
- [ ] Make initial commit: `Initial commit: project structure and requirements`

### Recommended folder structure
```
/store_app/
  main.py              ← entry point
  db.py                ← database connection + queries
  auth.py              ← login logic, session, timeout
  ui/
    login_frame.py     ← login screen
    dashboard_frame.py ← main dashboard (role-based)
    manager_frame.py   ← manager-only views
    employee_frame.py  ← employee views
  utils/
    validator.py       ← input validation helpers
    constants.py       ← colors, fonts, window size
requirements.txt
README.md
TODO.md
```

---

## Phase 2 — Database Setup
**Suggested assignee: Michael**

- [ ] Create MySQL database `store_db`
- [ ] Create `Users` table:
  ```sql
  CREATE TABLE Users (
      user_id     INT AUTO_INCREMENT PRIMARY KEY,
      username    VARCHAR(50) UNIQUE NOT NULL,
      password_hash VARCHAR(255) NOT NULL,
      role        ENUM('manager', 'employee') NOT NULL,
      created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
  ```
- [ ] Create `LoginHistory` table (for username autocomplete):
  ```sql
  CREATE TABLE LoginHistory (
      id        INT AUTO_INCREMENT PRIMARY KEY,
      username  VARCHAR(50) NOT NULL,
      logged_in_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
  ```
- [ ] Write `db.py` — connection function with error handling
- [ ] Write `db.py` — `get_user(username)` query
- [ ] Write `db.py` — `create_user(username, password_hash, role)` query
- [ ] Write `db.py` — `get_recent_usernames()` for autocomplete
- [ ] Seed one manager account for testing
- [ ] Commit: `Added database schema and db.py connection module`

---

## Phase 3 — Auth Logic
**Suggested assignee: Michael**

- [ ] Write `auth.py` — `hash_password(password)` using `hashlib` or `bcrypt`
- [ ] Write `auth.py` — `verify_login(username, password)` — checks DB, returns user role or None
- [ ] Write `auth.py` — `create_account(username, password, role)` — managers only
- [ ] Write `auth.py` — inactivity timeout logic (track last action time, auto-logout after X seconds)
- [ ] Commit: `Added auth module: login verification, password hashing, timeout logic`

---

## Phase 4 — Login Screen
**Suggested assignee: Creed**

- [x] Build `login_frame.py` — username field with autocomplete (pulls from `LoginHistory`)
- [x] Build `login_frame.py` — password field (masked)
- [x] Build `login_frame.py` — "Sign In" button → calls `verify_login()` → routes by role
- [x] Build `login_frame.py` — "Create Account" button (visible to managers only / on first run)
- [x] Build `login_frame.py` — error message label (invalid credentials, empty fields)
- [x] Add input validation: empty username, empty password, username length limit
- [x] Style to match design standards (colors, font, window size)
- [x] Commit: `Added login screen with autocomplete and input validation`

---

## Phase 5 — Role-Based Dashboard
**Suggested assignee: Creed**

- [ ] Build `dashboard_frame.py` — base layout with sidebar navigation
- [ ] Build `manager_frame.py` — manager view: shows all nav items (Dashboard, Products, Categories, Suppliers, Inventory, Customers, Orders, Returns)
- [ ] Build `employee_frame.py` — employee view: limited nav (Dashboard, Orders, Inventory only)
- [ ] Wire role routing: after login, load correct frame based on `role` from DB
- [ ] Add logout button → clears session, returns to login screen
- [ ] Commit: `Added role-based dashboard: manager and employee views`

---

## Phase 6 — Inactivity Timeout
**Suggested assignee: Michael**

- [ ] Bind mouse + keyboard events to reset inactivity timer
- [ ] On timeout: show warning popup ("You will be logged out in 60 seconds")
- [ ] On confirmed timeout: clear session and redirect to login screen
- [ ] Make timeout duration a constant in `constants.py` (easy to adjust)
- [ ] Commit: `Added inactivity timeout with warning popup`

---

## Phase 7 — Polish & Rubric Checks
*Do this together before final submission*

- [ ] Verify all input fields have validation + error messages
- [ ] Verify consistent colors, fonts, and window size across all screens (use `constants.py`)
- [ ] Add docstrings and inline comments to every function
- [ ] Review commit history — make sure both members have meaningful commits
- [ ] Test: login with manager account → see manager view
- [ ] Test: login with employee account → see employee view
- [ ] Test: wrong password → error message shown
- [ ] Test: inactivity timeout triggers correctly
- [ ] Test: username autocomplete suggests previous usernames
- [ ] Test: manager can create new account, employee cannot
- [ ] Final commit: `Finalized Activity 4 submission`

---

## Design Standards (from Activity 3 — keep consistent)

| Property | Value |
|---|---|
| Window size | 1280 × 800 |
| Font | Segoe UI (or Helvetica as fallback) |
| Primary color | `#2C3E50` |
| Action color | `#3498DB` |
| Alert color | `#E74C3C` |
| Background | `#F5F5F5` |

---

## Rubric Coverage Checklist

- [ ] GitHub repo created, instructor added, regular commits
- [ ] Both members have meaningful individual commits
- [ ] All functions are commented
- [ ] Code is modular (no large unstructured blocks)
- [ ] Login page verifies credentials and routes by role
- [ ] Manager and employee see different interfaces
- [ ] Navigation between screens is smooth
- [ ] Layout is consistent across all screens
- [ ] All input fields validate and show error messages
- [ ] SQL DB supports user registration and login verification
