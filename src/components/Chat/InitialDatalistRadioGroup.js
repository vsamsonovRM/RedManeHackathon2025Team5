import React from "react";

function InitialDatalistRadioGroup({ options, selectedOption, updateState, onSelect }) {
  return (
    <div role="radiogroup" aria-label="Datalist options" className="chat-radio-group">
      {options.map(opt => (
        <label key={opt.id} style={{ display: 'block', margin: '0.3em 0' }}>
          <input
            type="radio"
            name="datalist"
            value={opt.id}
            checked={selectedOption === opt.id}
            disabled={updateState}
            onChange={onSelect}
            style={{ marginRight: 8 }}
          />
          {opt.label}
        </label>
      ))}
    </div>
  );
}

export default InitialDatalistRadioGroup;
