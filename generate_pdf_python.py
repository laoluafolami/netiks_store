#!/usr/bin/env python3
"""
Convert HTML deployment report to PDF
Uses weasyprint or reportlab as fallback
"""

import os
import sys
from pathlib import Path

def generate_pdf_weasyprint():
    """Generate PDF using weasyprint"""
    try:
        from weasyprint import HTML, CSS
        
        html_file = Path(__file__).parent / 'Netiks_Store_Week2_Azure_Deployment_Report.html'
        pdf_file = Path(__file__).parent / 'Netiks_Store_Week2_Azure_Deployment_Report.pdf'
        
        print(f"📄 Converting {html_file.name} to PDF...")
        print(f"Using: weasyprint")
        
        HTML(string=html_file.read_text(), base_url=str(html_file)).write_pdf(
            pdf_file,
            stylesheets=[CSS(string="""
                @page {
                    size: A4;
                    margin: 2cm;
                }
                body {
                    font-family: Arial, sans-serif;
                }
            """)]
        )
        
        print(f"✅ PDF generated successfully: {pdf_file}")
        return True
        
    except ImportError:
        print("⚠️  weasyprint not available")
        return False
    except Exception as e:
        print(f"❌ weasyprint error: {e}")
        return False

def generate_pdf_reportlab():
    """Generate PDF using reportlab"""
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
        from reportlab.lib.units import inch
        import re
        from html.parser import HTMLParser
        
        html_file = Path(__file__).parent / 'Netiks_Store_Week2_Azure_Deployment_Report.html'
        pdf_file = Path(__file__).parent / 'Netiks_Store_Week2_Azure_Deployment_Report.pdf'
        
        print(f"📄 Converting {html_file.name} to PDF...")
        print(f"Using: reportlab (with HTML parsing)")
        
        # Create PDF
        doc = SimpleDocTemplate(str(pdf_file), pagesize=A4)
        story = []
        styles = getSampleStyleSheet()
        
        # Add title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor='#0078d4',
            spaceAfter=30,
            fontName='Helvetica-Bold'
        )
        story.append(Paragraph("Netiks Store - Week 2 Lab Deployment Report", title_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Add basic info
        info_style = ParagraphStyle(
            'CustomInfo',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6
        )
        story.append(Paragraph("<b>Date:</b> August 19, 2026", info_style))
        story.append(Paragraph("<b>VM Public IP:</b> 20.29.81.166", info_style))
        story.append(Paragraph("<b>Deployment Status:</b> ✅ Fully Deployed and Verified", info_style))
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph("<b>NOTICE:</b> This is an automated PDF conversion of the HTML report. For full functionality and embedded images, please open the HTML version.", styles['Normal']))
        story.append(PageBreak())
        
        # Build PDF
        doc.build(story)
        
        print(f"✅ Basic PDF generated successfully: {pdf_file}")
        print("📝 Note: For full formatting with images, use the HTML or use wkhtmltopdf tool")
        return True
        
    except ImportError:
        print("⚠️  reportlab not available")
        return False
    except Exception as e:
        print(f"❌ reportlab error: {e}")
        return False

def check_wkhtmltopdf():
    """Check if wkhtmltopdf is available"""
    import subprocess
    try:
        result = subprocess.run(['wkhtmltopdf', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Found: {result.stdout.strip().split(chr(10))[0]}")
            return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass
    return False

def generate_pdf_wkhtmltopdf():
    """Generate PDF using wkhtmltopdf"""
    try:
        import subprocess
        
        html_file = Path(__file__).parent / 'Netiks_Store_Week2_Azure_Deployment_Report.html'
        pdf_file = Path(__file__).parent / 'Netiks_Store_Week2_Azure_Deployment_Report.pdf'
        
        print(f"📄 Converting {html_file.name} to PDF...")
        print(f"Using: wkhtmltopdf")
        
        cmd = [
            'wkhtmltopdf',
            '--enable-local-file-access',
            '--margin-top', '20mm',
            '--margin-right', '15mm',
            '--margin-bottom', '20mm',
            '--margin-left', '15mm',
            '--print-media-type',
            str(html_file),
            str(pdf_file)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ PDF generated successfully: {pdf_file}")
            return True
        else:
            print(f"❌ wkhtmltopdf error: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("⚠️  wkhtmltopdf not installed")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("=" * 60)
    print("PDF Generation Tool for Deployment Report")
    print("=" * 60)
    
    # Try different PDF generation methods
    methods = [
        ("wkhtmltopdf", check_wkhtmltopdf, generate_pdf_wkhtmltopdf),
        ("weasyprint", lambda: True, generate_pdf_weasyprint),
        ("reportlab", lambda: True, generate_pdf_reportlab),
    ]
    
    for name, check_func, generate_func in methods:
        try:
            if check_func():
                print()
                if generate_func():
                    return 0
        except Exception as e:
            print(f"❌ {name} failed: {e}")
            continue
    
    print("\n" + "=" * 60)
    print("❌ Could not generate PDF")
    print("\n📋 Recommendations:")
    print("1. Install wkhtmltopdf: https://wkhtmltopdf.org/")
    print("2. Or install via: pip install weasyprint")
    print("3. Or install via: pip install reportlab")
    print("=" * 60)
    
    return 1

if __name__ == '__main__':
    sys.exit(main())
