import axios from 'axios';
export async function selectTopDatalist(selectedRecord) {
  try {
    const res = await axios.post("/api/selected-record", { selectedRecord });
    return res;
  } catch (err) {
    console.error("Error selecting record:", err);
    return { response: "Error selecting record." };
  }
}