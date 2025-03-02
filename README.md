# User Management Application

This project is a user management application built with Python, supporting both REST and gRPC interfaces, PostgreSQL for the database, and JWT authentication. The entire setup is containerized using Docker Compose.

---

## 📦 Features

- REST API with FastAPI
- gRPC service
- PostgreSQL database
- JWT authentication
- Health checks for gRPC
- Unit tests using pytest(due to lack of time not able to implement)
- Docker Compose for easy setup

---

## 🚀 Getting Started

### 1. **Clone the repository**

```bash
git clone <repository-url>
cd <project-directory>
```

### 2. **Set up environment variables**

Create a `.env` file with the following variables:

```dotenv
DATABASE_URL=postgresql://postgres:password@postgres:5432/userdb
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. **Build and run the services**

Use Docker Compose to build and start the containers:

```bash
docker-compose up --build
```

This will start the following services:

- **REST API** on [http://localhost:8000](http://localhost:8000)
- **REST API Swagger Docs** on [http://localhost:8000/docs](http://localhost:8000/docs)
- **gRPC Service** on localhost:50051
- **PostgreSQL** on localhost:5432

```

---

## 📡 Test Health check and Endpoints

To check the Enpoints run:

```bash
python test_rest.py
```


```bash
python test_grpc.py
```
---

## 🛠️ Stopping the application

To stop all running containers:

```bash
docker-compose down
```

---

## 🔧 Useful Commands

- **Rebuild and run**: `docker-compose up --build`
- **Stop services**: `docker-compose down`
- **View logs**: `docker-compose logs -f`

---

## 📚 Contributing

1. Fork the repo
2. Create a new branch (`git checkout -b feature/awesome-feature`)
3. Commit changes (`git commit -m 'Add some awesome feature'`)
4. Push to the branch (`git push origin feature/awesome-feature`)
5. Open a pull request

---


