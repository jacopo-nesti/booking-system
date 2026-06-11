# BOOKING SYSTEM - Appointment Booking Web App

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-web%20framework-black)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-active-success)

---

## Project description

This is a full-stack appointment booking web application built with **Flask** for service-based businesses. The core architecture is reusable and can be adapted for other service-based businesses. This project is designed for a hair salon.

It allows users to browse services, select available time slots, and book appointments. The system handles authentication, scheduling, and booking management with a structured workflow that prevents conflicts.

An admin dashboard provides full control over services and bookings, including creation, updates, and deletion of treatments.

---

## Preview

*Work in progress*

---

## Features (MVP)

- Full appointment booking system for service-based businesses
- Secure user authentication with password hashing
- Email validation using standard regex patterns
- Service and pricing management
- Availability scheduling and time slot management
- Admin dashboard for managing bookings (add new, remove and modify service)
- Advanced admin filtering for bookings and treatments
- Responsive UI for desktop use

---

## Tech stack

| Layer    | Technology                                                                         |
| -------- | ---------------------------------------------------------------------------------- |
| Backend  | Python 3.10+, Flask 3                                                              |
| Database | SQLite (sqlite3)                                                                   |
| Frontend | HTML, CSS, Jinja2 templates                                                        |
| Security | Werkzeug password hashing, session authentication, Flask login_required protection |


---

## Technical Features

- Secure authentication with password hashing using Werkzeug  
- Session-based login system  
- Route protection using `login_required` decorators  
- Email validation using standard regex patterns  
- CRUD operations for services and bookings  
- SQLite database integration for data persistence  
- Jinja2 template rendering for dynamic pages  
- Clean Flask routing structure for core application logic  
---

## Project Structure

For the project structure, refer to the [Structure](/docs/STRUCTURE.md) file.

---

## Preview

*Work in progress*

---

## Installation and Setup

Refer to the [Installation Guide](/docs/INSTALLATION.md) for detailed setup instructions.

---

## Flask Routes

### Public Routes
| Route        | Methods | Description                           |
| ------------ | ------- | ------------------------------------- |
| `/`          | GET     | Home page                             |
| `/contacts`  | GET     | Contact page                          |
| `/selection` | GET     | Display available treatments/services |

### Authentication
| Route       | Methods   | Description                        |
| ----------- | --------- | ---------------------------------- |
| `/register` | GET, POST | User registration with validation  |
| `/login`    | GET, POST | User login with session management |
| `/logout`   | GET       | Clear session and log out user     |

### Booking System
| Route                                         | Methods   | Description                           |
| --------------------------------------------- | --------- | ------------------------------------- |
| `/book`                                       | GET, POST | Create a new booking (login required) |
| `/availability`                               | GET       | Redirect to availability page         |
| `/availability/<booking_date>/<treatment_id>` | GET       | Show available time slots             |

### User Dashboard
| Route        | Methods | Description                                   |
| ------------ | ------- | --------------------------------------------- |
| `/dashboard` | GET     | User dashboard with bookings (login required) |

## Admin Panel
| Route                                     | Methods   | Description                     |
| ----------------------------------------- | --------- | ------------------------------- |
| `/admin/dashboard`                        | GET       | Overview of all bookings        |
| `/admin/treatments`                       | GET       | Manage services/treatments      |
| `/admin/treatments/create`                | GET, POST | Create new treatment/service    |
| `/admin/treatments/edit/<treatment_id>`   | GET, POST | Edit existing treatment/service |
| `/admin/treatments/delete/<treatment_id>` | POST      | Delete treatment/service        |

---

## Authors

- Jacopo Nesti

---

## License

© 2026 Jacopo Nesti. All rights reserved.
This project is shared for portfolio purposes only. No permission is granted to use, copy, modify, or distribute this software.

---

## My Roadmap for the project

If you'd like to see my roadmap, see [roadmap](/docs/roadmap.md). The file is in Italian.

---

## Future Roadmap

### MVP (current system foundation)
- Core booking system
- Authentication system (register/login)
- Admin dashboard for managing bookings and services
- Advanced admin filtering for bookings and treatments

### V2 (user experience improvements)
- Full user booking history
- Email verification and notifications
- Password recovery system
- Password manager
- Admin can add images to services

### V3 (scalability & monetization)
- Online payment integration
- Automated cleanup/archiving of past bookings
- Multi-business / multi-tenant architecture (SaaS evolution)
- Automated testing suite (unit + integration tests)
- Improve UI for mobile use