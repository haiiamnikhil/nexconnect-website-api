# NexConnect Website

## Goal

Build an attractive corporate website for NexConnect using Angular 19 (Material) and a FastAPI backend with PostgreSQL. The app features a dynamic product catalog, a contact form with dual SMTP emails, and secure JWT admin authentication.

## Tasks

- [x] Task 1: Setup PostgreSQL database with schema for AdminUsers, Products, and ContactSubmissions. → Verify: psql connection and schema existence.
- [x] Task 2: Setup Python venv and FastAPI project structure with SQLAlchemy and Pydantic. → Verify: `uvicorn backend.main:app` runs.
- [x] Task 3: Implement Auth (JWT) and Admin API endpoints (Products CRUD, Contact viewing). → Verify: Swagger UI shows secured endpoints and token generation works.
- [x] Task 4: Implement Public API endpoints (get products, submit contact with Jinja2 SMTP emails). → Verify: HTTP requests create records and trigger emails.
- [x] Task 5: Scaffold Angular 19 project, install Angular Material, and integrate "Champagne & Limousines" font. → Verify: `ng serve` starts and typography applies.
- [/] Task 6: Build UI Components and Pages (Home, Products, Contact) matching Google-like aesthetic. → Verify: Pages render correctly and consume public API endpoints.
- [ ] Task 7: Build Secure Admin Dashboard (Login, Products Manager, Contact Viewer). → Verify: Admin can log in, add products, and view messages.
- [ ] Task 8: Final integration testing, UI/UX audit, and performance checks. → Verify: `checklist.py` passes without critical errors.

## Done When

- [ ] End-to-end flow works: Guest views products, submits contact form, receives email.
- [ ] Admin logs in with JWT, manages products, and views submitted contacts.
