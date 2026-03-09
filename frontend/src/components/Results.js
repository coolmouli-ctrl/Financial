import React, { useState } from 'react';
import './Results.css';

function Results({ results }) {
  const [showBreakdown, setShowBreakdown] = useState(false);

  if (!results) {
    return null;
  }

  return (
    <div className="results-container">
      <div className="success-banner">
        <span className="success-icon">✅</span>
        <span>Calculation Complete!</span>
      </div>

      <div className="metrics-grid">
        <div className="metric-card primary">
          <div className="metric-label">Average Interest Rate</div>
          <div className="metric-value">{results.average.toFixed(2)}%</div>
        </div>

        <div className="metric-card">
          <div className="metric-label">Minimum Rate</div>
          <div className="metric-value">{results.min.toFixed(2)}%</div>
        </div>

        <div className="metric-card">
          <div className="metric-label">Maximum Rate</div>
          <div className="metric-value">{results.max.toFixed(2)}%</div>
        </div>

        <div className="metric-card">
          <div className="metric-label">Median Rate</div>
          <div className="metric-value">{results.median.toFixed(2)}%</div>
        </div>

        <div className="metric-card">
          <div className="metric-label">Standard Deviation</div>
          <div className="metric-value">{results.stdDev.toFixed(2)}%</div>
        </div>

        <div className="metric-card">
          <div className="metric-label">Total Records</div>
          <div className="metric-value">{results.count}</div>
        </div>
      </div>

      <div className="breakdown-section">
        <button
          className="breakdown-toggle"
          onClick={() => setShowBreakdown(!showBreakdown)}
        >
          {showBreakdown ? '▼' : '▶'} View Detailed Breakdown
        </button>

        {showBreakdown && (
          <div className="breakdown-content">
            <div className="table-wrapper">
              <table className="breakdown-table">
                <thead>
                  <tr>
                    <th>Row</th>
                    <th>Principal</th>
                    <th>Interest</th>
                    <th>Rate (%)</th>
                  </tr>
                </thead>
                <tbody>
                  {results.breakdown.map((item, index) => (
                    <tr key={index}>
                      <td>{item.row}</td>
                      <td>${item.principal.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
                      <td>${item.interest.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
                      <td className="rate-cell">{item.rate.toFixed(2)}%</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Results;
