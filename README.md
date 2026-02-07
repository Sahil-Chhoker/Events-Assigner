# Photographer Assignment System

A Django REST API for managing events and photographers, with automatic photographer assignment based on availability.
The system prevents double-booking, validates edge cases, and exposes a clean REST interface.

---

## What this does

* Manage **Events** and **Photographers**
* Automatically assign photographers to events
* Prevent photographers from being booked for multiple events on the same date
* Handle edge cases clearly (past events, insufficient photographers, duplicates)
* Provide predictable, well-structured API responses

---

## Core Features

* CRUD APIs for Events and Photographers
* Smart auto-assignment based on:

  * Event date
  * Photographer availability
  * Active status
* Conflict and double-booking prevention
* Clear validation errors and HTTP status codes
* Docker support

---

## Tech Stack

* Python 3.12.0
* Django 6.0
* Django REST Framework
* SQLite
* Docker & Docker Compose

---

## Assignment Logic (High Level)

When assigning photographers to an event:

1. **Validate**

   * `photographers_required > 0`
   * Event date is not in the past
   * Event has no existing assignments

2. **Find available photographers**

   * Only `is_active=True`
   * Exclude photographers already assigned to another event on the same date

3. **Check availability**

   * If available < required → return error

4. **Create assignments**

   * One assignment per photographer
   * Database enforces `(event, photographer)` uniqueness

---

## API Overview

### Events

| Method | Endpoint                                 | Description                            |
| ------ | ---------------------------------------- | -------------------------------------- |
| GET    | `/api/events/`                           | List events                            |
| POST   | `/api/events/`                           | Create event                           |
| GET    | `/api/events/{id}/`                      | Event details + assigned photographers |
| PUT    | `/api/events/{id}/`                      | Update event                           |
| DELETE | `/api/events/{id}/`                      | Delete event                           |
| POST   | `/api/events/{id}/assign-photographers/` | Auto-assign photographers              |
| GET    | `/api/events/{id}/assignments/`          | Event assignments                      |

### Photographers

| Method | Endpoint                            | Description           |
| ------ | ----------------------------------- | --------------------- |
| GET    | `/api/photographers/`               | List photographers    |
| POST   | `/api/photographers/`               | Create photographer   |
| GET    | `/api/photographers/{id}/`          | Photographer details  |
| PUT    | `/api/photographers/{id}/`          | Update photographer   |
| DELETE | `/api/photographers/{id}/`          | Delete photographer   |
| GET    | `/api/photographers/{id}/schedule/` | Photographer’s events |

---

## Error Handling Examples

**Not enough photographers**

```json
{
  "error": "Not enough photographers available",
  "required": 3,
  "available": 1
}
```

**Already assigned**

```json
{
  "error": "Photographers already assigned to this event",
  "assigned_count": 2
}
```

**Past event**

```json
{
  "error": "Cannot assign photographers to past events"
}
```

---

## Data Models

### Event

* `event_name`
* `event_date`
* `photographers_required`
* `created_at`

### Photographer

* `name`
* `email` (unique)
* `phone`
* `is_active`

### Assignment

* `event`
* `photographer`
* Unique `(event, photographer)`

---

## Setup (Local)

### Step-by-Step

Get the repo:
```bash
git clone https://github.com/Sahil-Chhoker/Events-Assigner.git
cd Events-Assigner
```

Create virtual env:
```bash
python -m venv env
```

Activate venv:
```bash
# for linux
source env/bin/activate
# for windows
.\env\Scripts\activate
```

Install dependencies:
```
pip install -r requirements.txt
```

Enter into working dir:
```
cd photographer_system/
```

Run migrations:
```
python manage.py migrate
python manage.py runserver
```

For sample data, run:
```bash
python manage.py create_sample_data
```
Creates:

* Active + inactive photographers
* Events with different requirements

### Using Docker

Build container and run:
```bash
docker-compose up --build
```

API runs at:
`http://127.0.0.1:8000/api/`

---

## Testing

You can test using:

```bash
python manage.py test events
```

Covered scenarios:

* Successful assignment
* Insufficient photographers
* Past events
* Re-assignment attempts
* Inactive photographers
* Date conflicts

---

## Notes

* No authentication yet (easy to add with DRF tokens/JWT)
* No pagination (intentional for simplicity)
* Designed to be readable, extendable, and production-ready
