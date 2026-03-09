import React, { useState } from 'react';
import './CalculationForm.css';

function CalculationForm({ columns, onCalculate, loading }) {
  const [principalColumn, setPrincipalColumn] = useState(columns[0] || '');
  const [interestColumn, setInterestColumn] = useState(columns[1] || '');
  const [interestType, setInterestType] = useState('amount');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (principalColumn && interestColumn) {
      onCalculate(principalColumn, interestColumn, interestType);
    }
  };

  return (
    <div className="calculation-form-container">
      <h2>⚙️ Configure Calculation</h2>
      
      <form onSubmit={handleSubmit} className="calculation-form">
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="principal-column">Principal Column</label>
            <select
              id="principal-column"
              value={principalColumn}
              onChange={(e) => setPrincipalColumn(e.target.value)}
              required
            >
              <option value="">Select column...</option>
              {columns.map((col) => (
                <option key={col} value={col}>
                  {col}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="interest-column">Interest Column</label>
            <select
              id="interest-column"
              value={interestColumn}
              onChange={(e) => setInterestColumn(e.target.value)}
              required
            >
              <option value="">Select column...</option>
              {columns.map((col) => (
                <option key={col} value={col}>
                  {col}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="form-group">
          <label>Interest Column Type</label>
          <div className="radio-group">
            <label className="radio-label">
              <input
                type="radio"
                name="interest-type"
                value="amount"
                checked={interestType === 'amount'}
                onChange={(e) => setInterestType(e.target.value)}
              />
              <span>Interest Amount (needs calculation)</span>
            </label>
            <label className="radio-label">
              <input
                type="radio"
                name="interest-type"
                value="rate"
                checked={interestType === 'rate'}
                onChange={(e) => setInterestType(e.target.value)}
              />
              <span>Interest Rate (%)</span>
            </label>
          </div>
        </div>

        <button type="submit" className="btn-primary" disabled={loading}>
          {loading ? 'Calculating...' : 'Calculate Average Interest Rate'}
        </button>
      </form>
    </div>
  );
}

export default CalculationForm;
