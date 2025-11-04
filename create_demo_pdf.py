#!/usr/bin/env python3
"""
Create a multi-page dummy PDF with sample text for demo purposes
"""
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import black, blue, red
import os

def create_demo_pdf():
    """Create a multi-page PDF with sample content"""
    
    # Create output path
    output_path = os.path.join(os.path.dirname(__file__), 'demo_document.pdf')
    
    # Create PDF document
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    story = []
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        textColor=black,
        alignment=1  # Center alignment
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        textColor=blue
    )
    
    normal_style = styles['Normal']
    normal_style.fontSize = 12
    normal_style.spaceAfter = 12
    
    # Page 1: Title Page
    story.append(Paragraph("SAMPLE DOCUMENT FOR SIGNATURE EXTRACTION", title_style))
    story.append(Spacer(1, 0.5*inch))
    
    story.append(Paragraph("Document Information", heading_style))
    story.append(Paragraph("• Document Type: Multi-page PDF for testing", normal_style))
    story.append(Paragraph("• Created: November 4, 2025", normal_style))
    story.append(Paragraph("• Purpose: Demo document for signature extraction testing", normal_style))
    story.append(Paragraph("• Pages: 5 pages of content", normal_style))
    
    story.append(Spacer(1, 0.5*inch))
    
    story.append(Paragraph("Instructions for Testing", heading_style))
    story.append(Paragraph("1. Use this document to test PDF signing features", normal_style))
    story.append(Paragraph("2. Place signatures on any of the 5 pages", normal_style))
    story.append(Paragraph("3. Test bulk signature placement across multiple pages", normal_style))
    story.append(Paragraph("4. Verify audit logging and coordinate tracking", normal_style))
    
    story.append(Spacer(1, 1*inch))
    
    # Signature areas for testing
    story.append(Paragraph("Sample Signature Areas:", heading_style))
    story.append(Paragraph("• Page 1: Top right corner (for testing single placement)", normal_style))
    story.append(Paragraph("• Page 2-5: Various positions for bulk testing", normal_style))
    
    story.append(PageBreak())
    
    # Page 2: Contract Terms
    story.append(Paragraph("SERVICE AGREEMENT", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("1. SERVICES", heading_style))
    story.append(Paragraph("The service provider agrees to provide the following services to the client:", normal_style))
    story.append(Paragraph("• Consultation services as requested", normal_style))
    story.append(Paragraph("• Technical support during business hours", normal_style))
    story.append(Paragraph("• Regular progress updates and reporting", normal_style))
    
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("2. PAYMENT TERMS", heading_style))
    story.append(Paragraph("Payment shall be made according to the following terms:", normal_style))
    story.append(Paragraph("• 50% payment due upon signing of this agreement", normal_style))
    story.append(Paragraph("• 25% payment due at project milestone completion", normal_style))
    story.append(Paragraph("• Final 25% payment due upon project completion", normal_style))
    
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Client Signature: _________________________", normal_style))
    story.append(Paragraph("Date: _________________________", normal_style))
    
    story.append(PageBreak())
    
    # Page 3: Technical Specifications
    story.append(Paragraph("TECHNICAL SPECIFICATIONS", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("System Requirements", heading_style))
    story.append(Paragraph("• Operating System: macOS 10.15 or later, Windows 10 or later", normal_style))
    story.append(Paragraph("• Memory: Minimum 8GB RAM, Recommended 16GB", normal_style))
    story.append(Paragraph("• Storage: 1GB available disk space", normal_style))
    story.append(Paragraph("• Network: Broadband internet connection required", normal_style))
    
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("Performance Metrics", heading_style))
    story.append(Paragraph("• Document Processing: Up to 100 pages per minute", normal_style))
    story.append(Paragraph("• Signature Extraction: Sub-second response time", normal_style))
    story.append(Paragraph("• PDF Generation: Average 2-3 seconds per document", normal_style))
    story.append(Paragraph("• Concurrent Users: Supports up to 10 simultaneous users", normal_style))
    
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Technical Lead Signature: _________________________", normal_style))
    story.append(Paragraph("Date: _________________________", normal_style))
    
    story.append(PageBreak())
    
    # Page 4: Project Timeline
    story.append(Paragraph("PROJECT TIMELINE", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Phase 1: Planning and Setup (Weeks 1-2)", heading_style))
    story.append(Paragraph("• Requirements gathering and analysis", normal_style))
    story.append(Paragraph("• System architecture design", normal_style))
    story.append(Paragraph("• Development environment setup", normal_style))
    
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Phase 2: Core Development (Weeks 3-6)", heading_style))
    story.append(Paragraph("• Backend API development", normal_style))
    story.append(Paragraph("• Frontend user interface implementation", normal_style))
    story.append(Paragraph("• Database schema design and implementation", normal_style))
    story.append(Paragraph("• Initial testing and quality assurance", normal_style))
    
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Phase 3: Testing and Deployment (Weeks 7-8)", heading_style))
    story.append(Paragraph("• Comprehensive system testing", normal_style))
    story.append(Paragraph("• User acceptance testing", normal_style))
    story.append(Paragraph("• Production deployment", normal_style))
    story.append(Paragraph("• Training and documentation", normal_style))
    
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Project Manager Signature: _________________________", normal_style))
    story.append(Paragraph("Date: _________________________", normal_style))
    
    story.append(PageBreak())
    
    # Page 5: Terms and Conditions
    story.append(Paragraph("TERMS AND CONDITIONS", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("1. CONFIDENTIALITY", heading_style))
    story.append(Paragraph("Both parties agree to maintain the confidentiality of all proprietary information shared during the course of this project.", normal_style))
    
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("2. INTELLECTUAL PROPERTY", heading_style))
    story.append(Paragraph("All work product created under this agreement shall be the property of the client upon full payment of all fees.", normal_style))
    
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("3. LIMITATION OF LIABILITY", heading_style))
    story.append(Paragraph("The service provider's liability shall be limited to the amount paid for services under this agreement.", normal_style))
    
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("4. GOVERNING LAW", heading_style))
    story.append(Paragraph("This agreement shall be governed by and construed in accordance with the laws of the State of California.", normal_style))
    
    story.append(Spacer(1, 0.5*inch))
    
    story.append(Paragraph("BY SIGNING BELOW, THE PARTIES AGREE TO THE TERMS AND CONDITIONS OUTLINED IN THIS AGREEMENT.", normal_style))
    
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("CLIENT:", normal_style))
    story.append(Paragraph("Signature: _________________________", normal_style))
    story.append(Paragraph("Print Name: _________________________", normal_style))
    story.append(Paragraph("Title: _________________________", normal_style))
    story.append(Paragraph("Date: _________________________", normal_style))
    
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("SERVICE PROVIDER:", normal_style))
    story.append(Paragraph("Signature: _________________________", normal_style))
    story.append(Paragraph("Print Name: _________________________", normal_style))
    story.append(Paragraph("Title: _________________________", normal_style))
    story.append(Paragraph("Date: _________________________", normal_style))
    
    # Build PDF
    doc.build(story)
    
    print(f"✅ Demo PDF created successfully: {output_path}")
    print("\nDocument Details:")
    print("• 5 pages of sample content")
    print("• Multiple signature areas for testing")
    print("• Professional contract-style layout")
    print("• Suitable for signature extraction and placement testing")
    
    return output_path

if __name__ == "__main__":
    try:
        pdf_path = create_demo_pdf()
        print(f"\n📄 Demo PDF ready for use: {pdf_path}")
    except Exception as e:
        print(f"❌ Error creating demo PDF: {e}")
        print("\nTo install required dependencies:")
        print("pip install reportlab")