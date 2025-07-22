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

    const fetchSearchResults = async () => {
      try {
        const response = await axios.post("/api/search", {
          search_term: searchTerm,
          data_list_id: 726,
        });
        // Assuming response.data is an array of options
        console.log(response.data)
        const searchResultsCurr = response.data.response.map((result, idx) => (
          <div key={idx}>RecordName: {result.recordName}</div> 
        ));
        setSearchResults(searchResultsCurr);
        
        
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
      />
      <div role="radiogroup" aria-label="Top 10 Datalist options" className="chat-radio-group">
        {searchResults}
      </div>
    </>
  );
}

export default Top10DatalistRadioGroup;
