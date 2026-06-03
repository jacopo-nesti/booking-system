# BOOKING SYSTEM - Appointment Booking Web App

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-web%20framework-black)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-active-success)

---

## Project description

This project is a web application designed to manage appointment bookings for a hair salon.

Users can select a service (treatment), choose an available date and time through an interactive calendar, and complete the booking by entering their personal details (first name, last name, and email). Each service has a variable duration, which is taken into account when calculating available time slots.

After completing the booking, the user receives a confirmation email.

The system also includes a restricted admin area, accessible only to the business owner, where all bookings can be viewed with full details to help organize and manage daily operations.

---

## Preview

*Work in progress*

---

## Features (MVP)

- Appointment booking creation
- Service (treatment) selection
- Time slot validation based on availability and service duration
- Admin dashboard for managing all bookings *(work in progress)*
- Email confirmation system *(work in progress)*

---

## Tech stack

| Layer    | Stack                         |
| -------- | ----------------------------- |
| Backend  | Python 3.10+, Flask 3         |
| Database | SQLite (`sqlite3`)            |
| Frontend | HTML, CSS, Jinja2             |
| Security | *Work in progress*            |

---

## Technical Features

- Full-stack architecture with clear separation between backend, frontend, and database
- Server-side rendering using Jinja2 templates
- Dynamic appointment slot management based on service duration
- Time slot availability validation to prevent overlapping bookings
- Lightweight data structure powered by SQLite
- Guided booking flow (service → date → time → confirmation)
- Dedicated admin area for centralized booking management *(in development)*
- Automated email confirmation system *(in development)*
- Scalable structure prepared for future user authentication features

---

## Project Structure

For the project structure, refer to the [Structure](/docs/STRUCTURE.md) file.

---

## Screenshot

*Work in progress*

---

## Installation and Setup

<<<<<<< HEAD
Refer to the [Installation Guide](/docs/INSTALLATION.md) for detailed setup instructions.
=======
Refer to the [Installation Guide](/INSTALLATION.md) for detailed setup instructions.
>>>>>>> 2b9458a8fcd9f27871702cb2548db04fe52b34fb

---

## Flask Routes

| Method | Route               | Description                                                         |
| ------ | ------------------- | ------------------------------------------------------------------- |
| GET    | `/`                 | Displays the homepage with available services and booking form      |
| GET    | `/treatments`       | Retrieves all available treatments from the database                |
| GET    | `/available-slots`  | Retrieves available time slots for a selected date and treatment    |
| POST   | `/bookings`         | Creates a new booking and stores it in the database                 |
| GET    | `/login`            | Displays the administrator login form                               |
| POST   | `/login`            | Validates credentials and starts an admin session                   |
| GET    | `/dashboard-admin`  | Displays the admin dashboard with all bookings and management tools |
| GET    | `/logout`           | Ends the admin session and redirects to login or homepage           |

---

## Authors & License

- Jacopo Nesti
- This project is released under the MIT License. See the [LICENSE](/LICENSE.md) file for more details.

---

## My Roadmap for the project

If you'd like to see my roadmap, see [roadmap](/docs/roadmap.md). The file is in Italian.

---

## Future improvements

- Login
- User Dashboard
- Test
- Database Migrations
- Cancellation of Reservations
- Modification of Reservations
- Email Reminder Notification (Day Before)
- Admin Panel with Date Filter
- CSV Export of Reservations
