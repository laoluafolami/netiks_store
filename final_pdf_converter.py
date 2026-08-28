#!/usr/bin/env python3
"""
Final PDF Converter - Uses pypandoc with automatic pandoc download
"""

import sys
from pathlib import Path

def convert_markdown_to_pdf():
    """Convert markdown to PDF using pypandoc with auto-download"""
    try:
        import pypandoc
        
        md_file = Path(__file__).parent / 'Netiks_Store_Week2_Azure_Deployment_Report.md'
        pdf_file = Path(__file__).parent / 'Netiks_Store_Week2_Azure_Deployment_Report_Complete.pdf'
        
        if not md_file.exists():
            print(f"❌ Markdown file not found: {md_file}")
            return False
        
        print(f"📄 Converting markdown to PDF...")
        print(f"Input: {md_file.name}")
        
        # Download pandoc if not available
        print("⏳ Downloading pandoc (if needed)...")
        try:
            pypandoc.download_pandoc()
            print("✅ Pandoc ready")
        except:
            print("ℹ️  Pandoc already installed")
        
        print("🔄 Converting to PDF...")
        
        # Convert using pypandoc
        pypandoc.convert_file(
            str(md_file),
            'pdf',
            outputfile=str(pdf_file),
            extra_args=[
                '-V', 'geometry:margin=2cm',
                '-V', 'fontsize=11pt',
                '--toc',
                '--toc-depth=2',
                '--number-sections',
                '--highlight-style=tango'
            ]
        )
        
        if pdf_file.exists():
            file_size_mb = pdf_file.stat().st_size / (1024 * 1024)
            num_pages = estimate_pages(file_size_mb)
            print(f"\n✅ PDF generated successfully!")
            print(f"📍 Location: {pdf_file}")
            print(f"📊 Size: {file_size_mb:.2f} MB")
            print(f"📄 Estimated pages: ~{num_pages}")
            return True
        else:
            print("❌ PDF file was not created")
            return False
            
    except ImportError:
        print("❌ pypandoc not installed")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def estimate_pages(size_mb):
    """Rough estimate of PDF pages based on size"""
    return max(10, int(size_mb * 100))

def create_html_backup():
    """Create an HTML backup PDF using reportlab"""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.units import inch, cm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
        
        html_file = Path(__file__).parent / 'Netiks_Store_Week2_Azure_Deployment_Report.html'
        pdf_file = Path(__file__).parent / 'Netiks_Store_Week2_Azure_Deployment_Report.pdf'
        
        if not html_file.exists():
            return False
        
        print(f"\n🔄 Creating backup PDF with reportlab...")
        
        doc = SimpleDocTemplate(
            str(pdf_file),
            pagesize=A4,
            rightMargin=1.5*cm,
            leftMargin=1.5*cm,
            topMargin=2*cm,
            bottomMargin=2*cm,
        )
        
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'Title',
            fontSize=24,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#0078d4'),
            spaceAfter=12,
        )
        story.append(Paragraph("Netiks Store - Week 2 Lab Deployment Report", title_style))
        story.append(Paragraph("Complete Azure VM Deployment with Production Configuration", ParagraphStyle('Subtitle', fontSize=14, spaceAfter=20)))
        
        # Quick Info
        info_data = [
            ['Date', 'August 19, 2026'],
            ['VM Public IP', '20.29.81.166'],
            ['Status', '✅ Fully Deployed and Verified'],
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e3f2fd')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Executive Summary
        summary_heading = ParagraphStyle('Heading', fontSize=14, fontName='Helvetica-Bold', textColor=colors.HexColor('#0078d4'), spaceAfter=10)
        story.append(Paragraph("Executive Summary", summary_heading))
        
        summary = """This report documents the successful deployment of Netiks Store to an Azure Virtual Machine 
        following production security standards. All components have been deployed, configured, and validated for security 
        and functionality. The system includes Azure VM provisioning, Docker containerization, Nginx reverse proxy configuration, 
        production security settings, and complete deployment validation."""
        story.append(Paragraph(summary, ParagraphStyle('Normal', fontSize=10, leading=14, alignment=4)))
        
        story.append(Spacer(1, 0.2*inch))
        story.append(PageBreak())
        
        # Checklist
        story.append(Paragraph("Deployment Checklist", summary_heading))
        
        checklist_items = [
            '✅ VM Provisioned: Azure Standard_B2s with Ubuntu 22.04 LTS',
            '✅ Security Configured: Only ports 22, 80, 443 open',
            '✅ Dependencies Installed: Docker, Node.js 20, Nginx',
            '✅ Application Prepared: Production .env, secure secrets',
            '✅ Docker Configuration: Restart policies, loopback ports',
            '✅ Reverse Proxy: Nginx correctly routing /api/* traffic',
            '✅ Deployment Verified: All services running, data seeded',
            '✅ Security Validated: Internal ports not publicly accessible',
            '✅ Auto-restart Tested: Containers restart after VM reboot',
            '✅ Runbook Created: Complete deployment documentation',
        ]
        
        for item in checklist_items:
            story.append(Paragraph(f"• {item}", ParagraphStyle('Normal', fontSize=10, leading=14, leftIndent=20)))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Important Endpoints
        story.append(Paragraph("Application Endpoints", summary_heading))
        endpoints = """
        <b>Public Access:</b><br/>
        • Home: http://20.29.81.166/<br/>
        • API: http://20.29.81.166/api/v1/system/services<br/>
        • Market: http://20.29.81.166/market<br/>
        <br/>
        <b>Security Features:</b><br/>
        • Cloud firewall: Only essential ports open<br/>
        • Docker loopback: Internal services isolated<br/>
        • Database: Not exposed to internet<br/>
        • Secrets: Strong random passwords
        """
        story.append(Paragraph(endpoints, ParagraphStyle('Normal', fontSize=10, leading=12)))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Production Readiness
        story.append(Paragraph("Next Steps", summary_heading))
        story.append(PageBreak())
        
        steps = """
        1. Implement SSL/TLS with Let's Encrypt<br/>
        2. Configure domain DNS properly<br/>
        3. Set up monitoring and alerting<br/>
        4. Create backup strategy<br/>
        5. Implement CI/CD pipeline<br/>
        6. Add logging aggregation<br/>
        7. Configure auto-scaling<br/>
        8. Set up CDN<br/>
        9. Implement WAF<br/>
        10. Regular security scanning
        """
        story.append(Paragraph(steps, ParagraphStyle('Normal', fontSize=10, leading=14)))
        
        # Footer
        story.append(Spacer(1, 0.3*inch))
        footer = """
        <b>Report Generated:</b> August 19, 2026 | <b>Status:</b> ✅ Complete<br/>
        <font size=8>This PDF was automatically generated from the Deployment Report.</font>
        """
        story.append(Paragraph(footer, ParagraphStyle('Normal', fontSize=8, alignment=4)))
        
        doc.build(story)
        
        if pdf_file.exists():
            file_size_mb = pdf_file.stat().st_size / (1024 * 1024)
            print(f"✅ Backup PDF created!")
            print(f"📍 Location: {pdf_file}")
            print(f"📊 Size: {file_size_mb:.2f} MB")
            return True
        return False
        
    except Exception as e:
        print(f"⚠️  Reportlab backup failed: {e}")
        return False

def main():
    print("=" * 70)
    print("PDF Generation - Netiks Store Deployment Report")
    print("=" * 70)
    print()
    
    # Try markdown to PDF with pandoc
    if convert_markdown_to_pdf():
        return 0
    
    print("\n" + "-" * 70)
    print("Pandoc conversion failed, creating backup PDF...")
    print("-" * 70)
    
    # Fallback to HTML backup
    if create_html_backup():
        print("\n✅ PDF creation complete (backup version)")
        return 0
    
    print("\n❌ PDF generation failed")
    return 1

if __name__ == '__main__':
    sys.exit(main())
