import React from "react";

function Top10DatalistRadioGroup({ options, selectedOption, updateState, onSelect }) {
  return (
    <>
    <input type="text" placeholder="Select a top 10 datalist option"></input>
    <div role="radiogroup" aria-label="Top 10 Datalist options" className="chat-radio-group">
      {options.map(opt => (
        <label key={opt} style={{ display: 'block', margin: '0.3em 0' }}>
          <input
            type="radio"
            name="top10datalist"
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
    </>
    
  );
}

export default Top10DatalistRadioGroup;
