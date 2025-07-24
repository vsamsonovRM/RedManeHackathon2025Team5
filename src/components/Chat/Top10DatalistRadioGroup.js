import React, { useState, useEffect } from "react";
import axios from "axios";

function Top10DatalistRadioGroup({ options, selectedOption, updateState, onSelect }) {
  const [searchTerm] = useState("");
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
        setSearchResults(response.data.response);
      } catch (error) {
        console.error("Search API error:", error);
        // optionally reset or handle error state
      }
    };

    fetchSearchResults();
  }, [searchTerm, options]);


  return (
      <div role="radiogroup" aria-label="Top 10 Datalist options" className="chat-radio-group">

        {searchResults.map((opt,index) => (
          
          <label key={opt} style={{ display: "block", margin: "0.3em 0" }}>
            <input
              type="radio"
              name="top10datalist"
              id={index}
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

export default Top10DatalistRadioGroup;
