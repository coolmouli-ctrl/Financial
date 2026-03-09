import React, { useCallback } from 'react';
import './FileUpload.css';

function FileUpload({ onFileUpload, loading }) {
  const handleFileChange = useCallback((event) => {
    const file = event.target.files[0];
    if (file) {
      onFileUpload(file);
    }
  }, [onFileUpload]);

  const handleDrop = useCallback((event) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    if (file) {
      onFileUpload(file);
    }
  }, [onFileUpload]);

  const handleDragOver = useCallback((event) => {
    event.preventDefault();
  }, []);

  return (
    <div className="file-upload-container">
      <div
        className="file-upload-zone"
        onDrop={handleDrop}
        onDragOver={handleDragOver}
      >
        <div className="upload-icon">📁</div>
        <h2>Upload Excel File</h2>
        <p>Drag and drop your file here or click to browse</p>
        
        <label htmlFor="file-input" className="btn-primary">
          {loading ? 'Uploading...' : 'Choose File'}
        </label>
        <input
          id="file-input"
          type="file"
          accept=".xlsx,.xls"
          onChange={handleFileChange}
          disabled={loading}
          style={{ display: 'none' }}
        />
        
        <div className="file-info">
          <p>Supported formats: .xlsx, .xls</p>
          <p>Maximum file size: 16MB</p>
        </div>
      </div>

      <div className="example-format">
        <h3>📝 Expected Excel Format</h3>
        <table>
          <thead>
            <tr>
              <th>Principal</th>
              <th>Interest</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>10000</td>
              <td>500</td>
            </tr>
            <tr>
              <td>20000</td>
              <td>1200</td>
            </tr>
            <tr>
              <td>15000</td>
              <td>900</td>
            </tr>
          </tbody>
        </table>
        <p className="note">
          <strong>Note:</strong> Column names can be different (you'll select them in the app).
          Interest can be either the amount or the rate percentage.
        </p>
      </div>
    </div>
  );
}

export default FileUpload;
