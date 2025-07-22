import axios from 'axios';
export async function selectTopDatalist(selectedRecord) {
  try {
    const res = await axios.post("/api/selected-record", { selectedRecord });
    console.log("Selected Record Response:", res.data);
    return res.response;
  } catch (err) {
    console.error("Error selecting record:", err);
    return { response: "Error selecting record." };
  }
}