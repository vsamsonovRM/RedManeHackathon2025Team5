import React from 'react';
import axios from 'axios';

const sampleContent = {
  "headerFields": [
    { "label": "Last Name", "value": "Doe" },
    { "label": "First Name", "value": "John" },
    { "label": "Date of Birth", "value": "01/01/1990" },
    { "label": "Gender Identity", "value": "Male" }
  ],
  "content": [
    { "header": "Title", "body": "Lorem ipsum dolor sit amet." },
    { "header": "Title 2", "body": "Lorem ipsum again." }
    // etc...
  ],
  "defaultHeader": {
    "image": "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png",
    "title": "Screening Form",
    "description": "Optional subtitle or description"
  }
};

async function downloadDynamicPdf(content) {
  console.log("downloadDynamicPdf", content);
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
