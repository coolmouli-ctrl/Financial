import React from 'react';
import './DataPreview.css';

function DataPreview({ preview, totalRows }) {
  if (!preview || preview.length === 0) {
    return null;
  }

  const columns = Object.keys(preview[0]);

  return (
    <div className="data-preview-container">
      <h2>📋 Data Preview</h2>
      <p className="preview-info">
        Showing first {preview.length} of {totalRows} rows
      </p>
      
      <div className="table-wrapper">
        <table className="data-table">
          <thead>
            <tr>
              {columns.map((col) => (
                <th key={col}>{col}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {preview.map((row, index) => (
              <tr key={index}>
                {columns.map((col) => (
                  <td key={col}>{row[col] !== null ? row[col] : 'N/A'}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default DataPreview;
