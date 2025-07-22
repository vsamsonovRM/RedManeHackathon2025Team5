import React from "react";

function InitialDatalistRadioGroup({ options, selectedOption, updateState, onSelect }) {
  return (
    <div role="radiogroup" aria-label="Datalist options" className="chat-radio-group">
      {options.map(opt => (
        <label key={opt} style={{ display: 'block', margin: '0.3em 0' }}>
          <input
            type="radio"
            name="datalist"
            value={opt}
            checked={selectedOption === opt}
            disabled={updateState}
            onChange={onSelect}
            style={{ marginRight: 8 }}
          />
          {opt}
        </label>
      ))}
    </div>
  );
}

export default InitialDatalistRadioGroup;
