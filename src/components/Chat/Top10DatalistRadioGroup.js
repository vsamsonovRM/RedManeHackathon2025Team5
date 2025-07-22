import React, { useState, useEffect } from "react";
import axios from "axios";

function Top10DatalistRadioGroup({ options, selectedOption, updateState, onSelect }) {
  const [searchTerm, setSearchTerm] = useState("");
  const [searchResults, setSearchResults] = useState(options);


  useEffect(() => {
    if (searchTerm === "") {
      setSearchResults(options);
      return;
    }
    // Only search if searchTerm length >= 2
    if (searchTerm.length < 2) {
     
      return;
    }

    const fetchSearchResults = async () => {
      try {
        const response = await axios.post("/api/search", {
          search_term: searchTerm,
          data_list_id: 726,
        });
        setSearchResults(response.data.response.map(item => item.recordName));
      } catch (error) {
        console.error("Search API error:", error);
        // optionally reset or handle error state
      }
    };

    fetchSearchResults();
  }, [searchTerm, options]);

  const handleInputChange = (e) => {
    setSearchTerm(e.target.value);
  };

  return (
    <>
      <input
        type="text"
        placeholder="Select a top 10 datalist option"
        value={searchTerm}
        onChange={handleInputChange}
        style={{
          width: '100%',
          padding: '8px',
          marginBottom: '10px',
          border: '1px solid #ccc',
          borderRadius: '6px',
          fontSize: '1em',
          boxSizing: 'border-box',
          outline: 'none',
          transition: 'border-color 0.2s',
        }}
      />
      <div role="radiogroup" aria-label="Top 10 Datalist options" className="chat-radio-group">

        {searchResults.map((opt) => (
          <label key={opt} style={{ display: "block", margin: "0.3em 0" }}>
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
