from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch


def generate_pdf(name, age, symptoms, department, urgency, doctor, token, date):

    filename = f"Appointment_{token}.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    title = styles["Heading1"]
    title.alignment = TA_CENTER
    title.textColor = colors.darkblue

    heading = styles["Heading2"]
    heading.alignment = TA_CENTER

    normal = styles["BodyText"]

    story = []

    # ==========================
    # Hospital Header
    # ==========================

    story.append(Paragraph("🏥 SmartCare Hospital", title))
    story.append(Paragraph("Rajpur Road, Dehradun, Uttarakhand", normal))
    story.append(Paragraph("Phone: +91-9876543210", normal))
    story.append(Paragraph("Email: support@smartcare.ai", normal))

    story.append(Spacer(1, 0.3 * inch))

    story.append(Paragraph("<b>AI Hospital Appointment Slip</b>", heading))

    story.append(Spacer(1, 0.25 * inch))

    # ==========================
    # Patient Details Table
    # ==========================

    data = [
        ["Patient Name", name],
        ["Age", age],
        ["Symptoms", symptoms],
        ["Department", department],
        ["Urgency", urgency],
        ["Assigned Doctor", doctor],
        ["Appointment Token", token],
        ["Appointment ID", f"SC-{token}"],
        ["Date & Time", date],
    ]

    table = Table(data, colWidths=[2.3 * inch, 3.5 * inch])

    table.setStyle(TableStyle([

        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),

        ("GRID", (0,0), (-1,-1), 1, colors.grey),

        ("BACKGROUND", (0,0), (0,-1), colors.whitesmoke),

        ("TEXTCOLOR", (0,0), (-1,-1), colors.black),

        ("FONTNAME", (0,0), (-1,-1), "Helvetica"),

        ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),

        ("BOTTOMPADDING", (0,0), (-1,-1), 8),

        ("TOPPADDING", (0,0), (-1,-1), 8),

        ("VALIGN", (0,0), (-1,-1), "MIDDLE")

    ]))

    story.append(table)

    story.append(Spacer(1, 0.3 * inch))

    # ==========================
    # Emergency Message
    # ==========================

    if urgency == "High":

        story.append(
            Paragraph(
                "<font color='red'><b>🚨 EMERGENCY CASE DETECTED</b></font>",
                heading
            )
        )

        story.append(
            Paragraph(
                "<font color='red'>Notify Emergency Ward Immediately.</font>",
                normal
            )
        )

        story.append(Spacer(1, 0.2 * inch))

    # ==========================
    # Instructions
    # ==========================

    story.append(Paragraph("<b>Instructions</b>", heading))

    story.append(
        Paragraph(
            """
            • Please arrive 15 minutes before your appointment.<br/>
            • Carry a valid Government ID.<br/>
            • Bring previous prescriptions/reports if available.<br/>
            • Follow the doctor's instructions carefully.
            """,
            normal,
        )
    )

    story.append(Spacer(1, 0.25 * inch))

    # ==========================
    # Footer
    # ==========================

    story.append(
        Paragraph(
            "<b>Thank you for choosing SmartCare Hospital.</b>",
            heading,
        )
    )

    story.append(
        Paragraph(
            "Get Well Soon! We wish you a speedy recovery.",
            normal,
        )
    )

    doc.build(story)

    return filename