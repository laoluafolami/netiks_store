#!/usr/bin/env python3
"""
Generate a well-formatted PDF from the Deployment Report
Uses weasyprint for best results (HTML to PDF converter)
"""

import sys
from pathlib import Path

def install_weasyprint():
    """Try to install weasyprint"""
    import subprocess
    print("Installing weasyprint for better PDF quality...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "weasyprint"])
        return True
    except:
        return False

def generate_pdf_weasyprint():
    """Generate PDF using weasyprint - best quality"""
    try:
        from weasyprint import HTML, CSS
        
        html_file = Path(__file__).parent / 'Netiks_Store_Week2_Azure_Deployment_Report.html'
        pdf_file = Path(__file__).parent / 'Netiks_Store_Week2_Azure_Deployment_Report.pdf'
        
        if not html_file.exists():
            print(f"❌ HTML file not found: {html_file}")
            return False
        
        print(f"📄 Converting to PDF using weasyprint...")
        print(f"Input: {html_file.name}")
        
        # Convert HTML to PDF
        HTML(filename=str(html_file)).write_pdf(str(pdf_file))
        
        if pdf_file.exists():
            file_size_mb = pdf_file.stat().st_size / (1024 * 1024)
            print(f"✅ PDF generated successfully!")
            print(f"📍 Location: {pdf_file}")
            print(f"📊 Size: {file_size_mb:.2f} MB")
            return True
        else:
            print("❌ PDF file was not created")
            return False
            
    except ImportError:
        print("⚠️  weasyprint not installed")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def generate_pdf_reportlab_enhanced():
    """Generate PDF using reportlab with better formatting"""
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch, cm
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, PageTemplate, Frame
        from reportlab.pdfgen import canvas
        
        html_file = Path(__file__).parent / 'Netiks_Store_Week2_Azure_Deployment_Report.html'
        pdf_file = Path(__file__).parent / 'Netiks_Store_Week2_Azure_Deployment_Report.pdf'
        
        if not html_file.exists():
            print(f"❌ HTML file not found: {html_file}")
            return False
        
        print(f"📄 Converting to PDF using reportlab...")
        print(f"Input: {html_file.name}")
        
        # Create PDF document
        doc = SimpleDocTemplate(
            str(pdf_file),
            pagesize=A4,
            rightMargin=1.5*cm,
            leftMargin=1.5*cm,
            topMargin=2*cm,
            bottomMargin=2*cm,
        )
        
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#0078d4'),
            spaceAfter=12,
            fontName='Helvetica-Bold',
            alignment=0
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#0078d4'),
            spaceAfter=8,
            spaceBefore=12,
            fontName='Helvetica-Bold',
            borderPadding=6,
            borderColor=colors.HexColor('#e0e0e0'),
            borderWidth=0.5,
            borderPaddingLeft=10,
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            leading=14,
            spaceAfter=6,
            alignment=4  # Justify
        )
        
        # Title
        story.append(Paragraph("🌐 Netiks Store - Week 2 Lab Deployment Report", title_style))
        story.append(Paragraph("Complete Azure VM Deployment with Production Configuration", styles['Heading2']))
        story.append(Spacer(1, 0.2*inch))
        
        # Header info table
        header_data = [
            ['Date', 'August 19, 2026'],
            ['VM Public IP', '20.29.81.166'],
            ['App URL', 'http://20.29.81.166/'],
            ['Deployment Status', '✅ Fully Deployed and Verified'],
        ]
        
        header_table = Table(header_data, colWidths=[2*inch, 4*inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e3f2fd')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        
        story.append(header_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Executive Summary
        story.append(Paragraph("Executive Summary", heading_style))
        summary_text = """This report documents the successful deployment of Netiks Store to an Azure Virtual Machine 
        following production security standards. The deployment includes:
        <br/>• Azure VM (Standard_B2s - 2 vCPUs, 4GB RAM)
        <br/>• Docker and Docker Compose with secure configuration
        <br/>• Nginx reverse proxy with proper security headers
        <br/>• Production .env configuration with strong secrets
        <br/>• All internal services secured (ports bound to loopback only)
        <br/>• Automatic container restart policies
        <br/>• Complete deployment validation and testing
        """
        story.append(Paragraph(summary_text, normal_style))
        story.append(PageBreak())
        
        # Add deployment checklist
        story.append(Paragraph("Deployment Checklist", heading_style))
        checklist_data = [
            ['✅', 'VM Provisioned: Azure Standard_B2s with Ubuntu 22.04 LTS'],
            ['✅', 'Security Configured: Only ports 22, 80, 443 open'],
            ['✅', 'Dependencies Installed: Docker, Node.js 20, Nginx'],
            ['✅', 'Application Prepared: Production .env, secure secrets'],
            ['✅', 'Docker Configuration: Restart policies, loopback ports'],
            ['✅', 'Reverse Proxy: Nginx correctly routing /api/* and other traffic'],
            ['✅', 'Deployment Verified: All services running, data seeded'],
            ['✅', 'Security Validated: Internal ports not publicly accessible'],
            ['✅', 'Auto-restart Tested: Containers restart after VM reboot'],
            ['✅', 'Runbook Created: Complete deployment documentation'],
        ]
        
        checklist_table = Table(checklist_data, colWidths=[0.3*inch, 5.7*inch])
        checklist_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#ddd')),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        story.append(checklist_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Application Access
        story.append(Paragraph("Application Access & Security", heading_style))
        access_text = """
        <b>🚀 Application Access:</b>
        <br/>• Home Page: <a href="http://20.29.81.166/">http://20.29.81.166/</a>
        <br/>• API Endpoint: <a href="http://20.29.81.166/api/v1/system/services">http://20.29.81.166/api/v1/system/services</a>
        <br/>• Market Page: <a href="http://20.29.81.166/market">http://20.29.81.166/market</a>
        <br/>
        <br/><b>🔒 Security Status:</b>
        <br/>• Cloud firewall: Only 22, 80, 443 open
        <br/>• Docker ports: Only web/gateway on loopback
        <br/>• Database: Not exposed to internet
        <br/>• Secrets: Strong random passwords in use
        <br/>• Headers: Security headers via Nginx
        """
        story.append(Paragraph(access_text, normal_style))
        
        story.append(PageBreak())
        
        # Production Readiness
        story.append(Paragraph("Next Steps for Complete Production Readiness", heading_style))
        steps_text = """
        1. Implement SSL/TLS with Let's Encrypt<br/>
        2. Configure domain DNS properly<br/>
        3. Set up monitoring and alerting<br/>
        4. Create backup strategy for database and uploads<br/>
        5. Implement CI/CD pipeline for automated deployments<br/>
        6. Add logging aggregation (ELK stack or similar)<br/>
        7. Configure auto-scaling for traffic spikes<br/>
        8. Set up CDN for static assets and images<br/>
        9. Implement WAF (Web Application Firewall)<br/>
        10. Regular security scanning and updates
        """
        story.append(Paragraph(steps_text, normal_style))
        
        # Footer
        story.append(Spacer(1, 0.3*inch))
        footer_text = """
        <b>Report Generated:</b> August 19, 2026 | 
        <b>Deployment Complete:</b> ✅ | 
        <b>Production Ready:</b> ⚠️ Requires SSL and domain configuration
        <br/>
        <font size=8>
        This PDF was automatically generated from the comprehensive Deployment Report. 
        For full details with embedded images, see the HTML version.
        </font>
        """
        story.append(Paragraph(footer_text, styles['Normal']))
        
        # Build PDF
        doc.build(story)
        
        if pdf_file.exists():
            file_size_mb = pdf_file.stat().st_size / (1024 * 1024)
            print(f"✅ PDF generated successfully!")
            print(f"📍 Location: {pdf_file}")
            print(f"📊 Size: {file_size_mb:.2f} MB")
            return True
        else:
            print("❌ PDF file was not created")
            return False
            
    except Exception as e:
        print(f"❌ Error with reportlab: {e}")
        return False

def main():
    print("=" * 70)
    print("PDF Generation Tool - Netiks Store Deployment Report")
    print("=" * 70)
    print()
    
    # Try weasyprint first (best quality)
    try:
        print("Attempting weasyprint conversion...")
        if generate_pdf_weasyprint():
            return 0
    except Exception as e:
        print(f"ℹ️  weasyprint attempt failed: {e}")
    
    # Fall back to reportlab
    print("\nAttempting reportlab conversion...")
    if generate_pdf_reportlab_enhanced():
        return 0
    
    print("\n" + "=" * 70)
    print("❌ PDF generation failed")
    print("\n📦 To improve PDF quality, install weasyprint:")
    print("   pip install weasyprint")
    print("=" * 70)
    
    return 1

if __name__ == '__main__':
    sys.exit(main())
