# Stage 1: Build the React Frontend
FROM node:18-alpine AS build-stage
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Build the FastAPI Backend and Serve
FROM python:3.10-slim
WORKDIR /app

# Copy backend requirements and install
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend/ ./

# Copy built frontend static files from Stage 1
COPY --from=build-stage /app/frontend/dist /app/static

# Set environment variable to run in production mode
ENV ENVIRONMENT=production

# Expose the port (Cloud Run defaults to 8080)
EXPOSE 8080

# Run the FastAPI application using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
