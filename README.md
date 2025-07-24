# Django B2BROKER API

[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue)](https://www.python.org/)  
[![Django Version](https://img.shields.io/badge/django-5.1%2B-green)](https://www.djangoproject.com/)  

A simple, extensible Django-based web API application for managing wallets, deposits, withdrawals, and transfers.  

---

## Summary

- **RESTful API** for wallet creation, balance inquiries, deposits, withdrawals, and transfers (transactions)
- **Atomic transactions** to ensure consistency  
- **Dockerized** for one‑command local setup  

---

## Prerequisites

- GNU Make - https://www.gnu.org/software/make/#download
- Docker deamon - https://docs.docker.com/get-started/get-docker/

---

## Installation quickstart

1. **Clone the repository**  
   ```bash
   git clone https://github.com/arifgarayev/b2broker-task
   cd b2broker-task


2. **Build Images & Run Containers**  
    ```
    make run-build


3. **API Schema & Doc**
 - **Navigate** to ```127.0.0.1:8000``` for **Swagger UI** definitions

