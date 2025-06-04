import streamlit as st
import json
import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors


def format_text(text):
    text = text.replace("⇒", "=>")
    if "=>" in text:
        before, after = text.split("=>", 1)
        return f"{before.strip()}<br/><i>{after.strip()}</i>"
    return text.strip()


def create_combined_pdf(word_list):
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    # H1 style – word title
    title_style = ParagraphStyle(
        name="WordTitle",
        fontSize=32,
        leading=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue,
        spaceAfter=20,
        fontName="Helvetica-Bold"
    )

    # H3 style – section headers
    h3_style = ParagraphStyle(
        name="Heading3",
        fontSize=16,
        leading=22,
        spaceAfter=12,
        fontName="Helvetica-Bold"
    )

    # Body text – list items
    body_style = ParagraphStyle(
        name="BodyText",
        fontSize=12,
        leading=20,
        spaceAfter=10,
        leftIndent=20
    )

    for i, word_data in enumerate(word_list):
        word_title = word_data['word'].title()
        elements.append(Paragraph(word_title, title_style))
        elements.append(Spacer(1, 6))

        elements.append(Paragraph("Meanings", h3_style))
        for meaning in word_data["meanings"]:
            formatted = format_text(meaning.strip())
            elements.append(Paragraph(f"{formatted}", body_style))
        elements.append(Spacer(1, 12))

        elements.append(Paragraph("Synonyms", h3_style))
        for synonym in word_data["synonyms"]:
            elements.append(Paragraph(f"• {synonym}", body_style))
        elements.append(Spacer(1, 12))

        elements.append(Paragraph("Antonyms", h3_style))
        for antonym in word_data["antonyms"]:
            elements.append(Paragraph(f"• {antonym}", body_style))
        elements.append(Spacer(1, 20))

        if i != len(word_list) - 1:
            elements.append(PageBreak())

    doc.build(elements)
    buffer.seek(0)
    return buffer


# --- Streamlit App ---
st.title("📘 JSON to Styled PDF")

uploaded_file = st.file_uploader("Upload your JSON file", type=["json"])

if uploaded_file:
    try:
        word_list = json.load(uploaded_file)
        st.success("✅ JSON loaded successfully.")

        if st.button("📄 Generate PDF"):
            date_str = datetime.now().strftime("%y%m%d")
            pdf_filename = f"{date_str}_words.pdf"
            pdf_bytes = create_combined_pdf(word_list)

            st.download_button(
                label=f"📥 Download PDF ({pdf_filename})",
                data=pdf_bytes,
                file_name=pdf_filename,
                mime="application/pdf"
            )
    except Exception as e:
        st.error(f"❌ Error: {e}")