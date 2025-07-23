import React from 'react';
import axios from 'axios';

const sampleContent = {

    // "headerFields": [
    //   { "label": "First Name", "value": "jane" },
    //   { "label": "Last Name", "value": "doe" },
    //   { "label": "Legal Name", "value": "jane  doe" },
    //   { "label": "Sex at Birth", "value": "female" },
    //   { "label": "Gender Identity", "value": "female" },
    //   { "label": "Date of Birth", "value": "2020-11-01" },
    //   { "label": "Date of Birth Available?", "value": "yes" },
    //   { "label": "Alias / Other Names", "value": "jane doe" }
    // ],
    // "content": [
    //   { "header": "Active PSA Alerts Count", "body": "[2 active psa]" },
    //   { "header": "Person ID", "body": "p1332642429" },
    //   { "header": "Person Status", "body": "draft" },
    //   { "header": "Background Check Requester", "body": "person" },
    //   { "header": "Datalist Type", "body": "person" },
    //   { "header": "County", "body": "alcorn" },
    //   { "header": "Known / Unknown Person", "body": "known" },
    //   { "header": "recordName", "body": "P1332642429: Jane Doe [2 ACTIVE PSA]" }
    // ],
    // "defaultHeader": {
    //   "image": "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png",
    //   "title": "SCREENING FORM",
    //   "description": "Bimaadiziwin Wiidookaagewin Cultural Program"
    // }
};

export async function prepareDynamicPdfContent(content) {
    try {
    console.log('content', content);
    const response = await axios.post('/api/generate_pdf_content', content);


    console.log('response', response);
    return response.data.response;
  } catch (error) { 
    console.error('Failed to prepare PDF content:', error);
    return null;
  }
}

export async function downloadDynamicPdf(content) {
  console.log("downloadDynamicPdf", content);
  try {
    // console.log('content', content);
    // const response = await axios.post('/api/generate_pdf_content', content);


    // console.log('response', response);

    const response2 = await axios.post('/api/generate-pdf', content , {
      responseType: 'blob',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    console.log('response2', response2);


    const blob = new Blob([response2.data], { type: 'application/pdf' });
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
