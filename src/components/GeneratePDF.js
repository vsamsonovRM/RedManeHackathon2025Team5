import React from 'react';
import axios from 'axios';

const sampleContent = [
  { header: "Title", body: "Lorem ipsum dolor sit amet." },
  { header: "Title 2", body: "Lorem ipsum again." },
  { header: "Title 3", body: "Lorem ipsum again." },
  { header: "Title 4", body: "Lorem ipsum again." },
  { header: "Title 5", body: "Lorem ipsum again." },
  { header: "Title 6", body: "Lorem ipsum again." },
  { header: "Title 7", body: "Lorem ipsum again." },
  { header: "Title 8", body: "Lorem ipsum again." },
];

async function downloadDynamicPdf(content) {
  try {
    const response = await axios.post('/generate-pdf', content, {
      responseType: 'blob',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const blob = new Blob([response.data], { type: 'application/pdf' });
    const url = window.URL.createObjectURL(blob);

    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'custom-content.pdf');
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error('Failed to generate PDF:', error);
  }
}

const GeneratePDF = ({ content = sampleContent }) => (
  <button className="pdf-btn" onClick={() => downloadDynamicPdf(content)}>
    Generate PDF
  </button>
);

export default GeneratePDF;
