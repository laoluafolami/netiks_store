// PDF Generation Script
// This script converts the HTML report to PDF using Puppeteer

const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

async function generatePDF() {
  let browser;
  try {
    console.log('Starting PDF generation...');
    
    // Launch browser
    browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    console.log('Browser launched');
    
    // Create new page
    const page = await browser.newPage();
    
    // Set viewport
    await page.setViewport({
      width: 1200,
      height: 1600
    });
    
    // Get absolute path to HTML file
    const htmlPath = path.join(__dirname, 'Netiks_Store_Week2_Azure_Deployment_Report.html');
    const htmlUrl = `file://${htmlPath.replace(/\\/g, '/')}`;
    
    console.log(`Loading HTML from: ${htmlUrl}`);
    
    // Go to HTML file
    await page.goto(htmlUrl, {
      waitUntil: 'networkidle0',
      timeout: 60000
    });
    
    console.log('HTML loaded, generating PDF...');
    
    // Generate PDF with proper settings
    const pdfPath = path.join(__dirname, 'Netiks_Store_Week2_Azure_Deployment_Report.pdf');
    
    await page.pdf({
      path: pdfPath,
      format: 'A4',
      margin: {
        top: '20mm',
        right: '15mm',
        bottom: '20mm',
        left: '15mm'
      },
      printBackground: true,
      displayHeaderFooter: true,
      headerTemplate: '<div style="font-size: 10px; margin: 0 15mm; width: 100%;"></div>',
      footerTemplate: '<div style="font-size: 9px; margin: 0 15mm; width: 100%; display: flex; justify-content: space-between;"><span></span><span><span class="pageNumber"></span> of <span class="totalPages"></span></span></div>',
      scale: 1
    });
    
    console.log(`✅ PDF generated successfully: ${pdfPath}`);
    
    // Close browser
    await browser.close();
    
    return pdfPath;
  } catch (error) {
    console.error('❌ Error generating PDF:', error.message);
    if (browser) {
      await browser.close();
    }
    process.exit(1);
  }
}

// Run the function
generatePDF().then(() => {
  console.log('Process completed successfully');
  process.exit(0);
}).catch((error) => {
  console.error('Failed:', error);
  process.exit(1);
});
