# Hotel Reservation Predictive Analytics Dashboard

A professional-grade web application for predicting hotel reservation cancellations and forecasting future booking demand using Artificial Neural Networks (ANN) and SARIMAX time-series models.

## 🚀 Features

- **Real-time Cancellation Prediction**: Enter reservation details to get an instant risk score and prediction.
- **Demand Forecasting**: Visualise 12-week booking demand trends based on historical data.
- **KPI Dashboard**: Monitor crucial metrics like "Current Booking Trend" and "Cancellation Risk".
- **Batch Processing**: Upload CSV files for bulk prediction analysis.
- **Modern UI/UX**: Sleek, glassmorphism-inspired dark mode dashboard built with Next.js and Tailwind CSS.
- **Dockerized Deployment**: Fully containerised setup with Docker Compose.

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python), TensorFlow/Keras (ANN), Statsmodels (SARIMAX), Pandas, Scikit-learn.
- **Frontend**: Next.js 14, TypeScript, Tailwind CSS, Recharts, Framer Motion, Lucide Icons.
- **Deployment**: Docker, Docker Compose.

## 📥 Getting Started

### Prerequisites

- Docker and Docker Compose installed.
- Python 3.11+ (if running locally without Docker).
- Node.js 18+ (if running locally without Docker).

### Option 1: Using Docker (Recommended)

1. Clone the repository.
2. Run the following command in the root directory:
   ```bash
   docker-compose up --build
   ```
3. Access the dashboard at `http://localhost:3000`.
4. API docs available at `http://localhost:8000/docs`.

### Option 2: Local Development

#### Backend Setup
1. Navigate to `backend`.
2. Install dependencies:
   ```bash
   pip install -r ../requirements.txt
   pip install fastapi uvicorn python-multipart joblib
   ```
3. Generate preprocessors (one-time):
   ```bash
   python ../export_preprocessor.py
   ```
4. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

#### Frontend Setup
1. Navigate to `frontend`.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

## 📊 Model Details

- **Artificial Neural Network (ANN)**: Multi-layer perceptron trained on 36,000+ records to predict boolean `booking_status`. Achieves ~85% accuracy.
- **SARIMAX**: Seasonal AutoRegressive Integrated Moving Average model for weekly demand forecasting.

## 📁 Project Structure

```text
├── backend/
│   ├── assets/          # Trained models and preprocessors
│   ├── main.py          # FastAPI application
│   ├── utils.py         # Model wrapper and logic
│   └── Dockerfile
├── frontend/
│   ├── src/             # Next.js source code
│   └── Dockerfile
├── export_preprocessor.py # Script to link dataset stats to API
├── docker-compose.yml
└── requirements.txt
```

---
*Developed for Foundations of Data Sciences - 2024.*
