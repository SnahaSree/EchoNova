# NOVA Architecture

## System Overview

NOVA follows a layered full-stack architecture.

```text
User
 ↓
React Frontend
 ↓
FastAPI API
 ↓
Application Services
 ↓
Domain Logic
 ↓
Repository Layer
 ↓
MongoDB Atlas