# Interest Rate Calculator - React + Flask

A modern web application to calculate average interest rates from Excel files.

## Project Structure

```
Financial/
├── backend/
│   ├── app.py                 # Flask API server
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileUpload.js
│   │   │   ├── FileUpload.css
│   │   │   ├── DataPreview.js
│   │   │   ├── DataPreview.css
│   │   │   ├── CalculationForm.js
│   │   │   ├── CalculationForm.css
│   │   │   ├── Results.js
│   │   │   └── Results.css
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   └── package.json
└── README.md
```

## Prerequisites

- Python 3.7 or higher
- Node.js 14 or higher
- npm (comes with Node.js)

## Setup Instructions

### 1. Backend Setup (Flask)

Open a terminal and navigate to the backend folder:

```bash
cd "c:\Users\coolm\OneDrive\Chandramouli\Git Clone\Financial\backend"
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Start the Flask server:

```bash
python app.py
```

The API server will run at: http://localhost:5000

### 2. Frontend Setup (React)

Open a NEW terminal and navigate to the frontend folder:

```bash
cd "c:\Users\coolm\OneDrive\Chandramouli\Git Clone\Financial\frontend"
```

Install Node.js dependencies:

```bash
npm install
```

Start the React development server:

```bash
npm start
```

The application will automatically open in your browser at: http://localhost:3000

## How to Use

1. **Upload Excel File**: Click or drag-and-drop your Excel file (.xlsx or .xls)
2. **Preview Data**: Review the first 10 rows of your data
3. **Select Columns**: Choose which columns contain Principal and Interest data
4. **Choose Type**: Select whether Interest is an amount or percentage
5. **Calculate**: Click the button to see average interest rate and statistics
6. **View Details**: Expand the breakdown to see individual row calculations

## Excel File Format

Your Excel file should have at least two columns:

| Principal | Interest |
|-----------|----------|
| 10000     | 500      |
| 20000     | 1200     |
| 15000     | 900      |

**Notes:**
- Column names can be anything (you'll select them in the app)
- Interest can be either:
  - Amount (e.g., 500 for $500 interest)
  - Rate (e.g., 5.0 for 5% rate)

## API Endpoints

### Health Check
- **GET** `/api/health`
- Returns server status

### Upload File
- **POST** `/api/upload`
- Upload Excel file and get column preview
- Body: multipart/form-data with 'file' field

### Calculate Rates
- **POST** `/api/calculate-from-data`
- Calculate average interest rate from data
- Body: JSON with fileData, principalColumn, interestColumn, interestType

## Troubleshooting

### Port Already in Use

**Backend (Port 5000):**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Frontend (Port 3000):**
React will automatically prompt to use a different port

### CORS Issues
Make sure flask-cors is installed and the Flask server is running

### Module Not Found
Make sure all dependencies are installed:
```bash
# Backend
pip install -r backend/requirements.txt

# Frontend
cd frontend
npm install
```

## Development

- Backend runs on port 5000 (Flask)
- Frontend runs on port 3000 (React development server)
- CORS is configured to allow cross-origin requests

## Building for Production

To create a production build of the React app:

```bash
cd frontend
npm run build
```

The optimized files will be in `frontend/build/`

## Support

For issues or questions, check:
- Backend logs in the terminal running Flask
- Browser console for frontend errors
- Network tab in browser DevTools for API calls
