import React, { useState } from 'react';
import './App.css';
import FileUpload from './components/FileUpload';
import DataPreview from './components/DataPreview';
import CalculationForm from './components/CalculationForm';
import Results from './components/Results';

function App() {
  const [fileData, setFileData] = useState(null);
  const [columns, setColumns] = useState([]);
  const [preview, setPreview] = useState([]);
  const [totalRows, setTotalRows] = useState(0);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileUpload = async (file) => {
    setLoading(true);
    setError(null);
    
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:5000/api/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to upload file');
      }

      const data = await response.json();
      setColumns(data.columns);
      setPreview(data.preview);
      setTotalRows(data.totalRows);
      setFileData(data.preview);
      setResults(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCalculate = async (principalColumn, interestColumn, interestType) => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:5000/api/calculate-from-data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          fileData: preview,
          principalColumn,
          interestColumn,
          interestType,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to calculate');
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFileData(null);
    setColumns([]);
    setPreview([]);
    setTotalRows(0);
    setResults(null);
    setError(null);
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>📊 Average Interest Rate Calculator</h1>
        <p>Upload an Excel file with Principal and Interest data to calculate the average interest rate</p>
      </header>

      <main className="app-main">
        {error && (
          <div className="error-message">
            <span className="error-icon">⚠️</span>
            {error}
          </div>
        )}

        {!fileData ? (
          <FileUpload onFileUpload={handleFileUpload} loading={loading} />
        ) : (
          <>
            <div className="action-buttons">
              <button onClick={handleReset} className="btn-secondary">
                Upload New File
              </button>
            </div>

            <DataPreview preview={preview} totalRows={totalRows} />

            <CalculationForm
              columns={columns}
              onCalculate={handleCalculate}
              loading={loading}
            />

            {results && <Results results={results} />}
          </>
        )}
      </main>

      <footer className="app-footer">
        <p>Upload .xlsx or .xls files • Maximum file size: 16MB</p>
      </footer>
    </div>
  );
}

export default App;
