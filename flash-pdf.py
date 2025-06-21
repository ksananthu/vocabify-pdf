import streamlit as st
import json
import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    ListFlowable, ListItem
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors


# --- Helper to split meaning and examples ---
def parse_meaning_and_examples(text):
    text = text.replace("⇒", "=>")
    parts = text.split("=>")

    meaning = parts[0].strip()
    examples = []

    for i in range(1, len(parts)):
        example = parts[i].strip()
        if '.' in example:
            sentence, rest = example.split('.', 1)
            sentence = sentence.strip() + '.'
            parts[i] = rest.strip()
        else:
            sentence = example.strip()

        if sentence:
            examples.append(sentence)

    return meaning, examples


# --- PDF Generator Function ---
def create_combined_pdf(word_list):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    # --- Styles ---
    title_style = ParagraphStyle(
        name="WordTitle",
        fontSize=28,
        leading=32,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#1a237e"),  # Indigo
        spaceAfter=18,
        fontName="Helvetica-Bold"
    )

    section_style = ParagraphStyle(
        name="SectionHeader",
        fontSize=16,
        leading=24,
        spaceAfter=10,
        fontName="Helvetica-Bold"
    )

    meaning_style = ParagraphStyle(
        name="MeaningText",
        fontSize=12,
        leading=20,
        spaceAfter=6,
        leftIndent=0,
        fontName="Helvetica-Bold",
        textColor=colors.black
    )

    example_style = ParagraphStyle(
        name="ExampleText",
        fontSize=11,
        leading=18,
        spaceAfter=4,
        fontName="Helvetica-Oblique"
        # textColor=colors.HexColor("#616161")
    )

    synonym_style = ParagraphStyle(
        name="SynonymText",
        fontSize=12,
        leading=20,
        leftIndent=15,
        textColor=colors.HexColor("#1b5e20")
    )

    antonym_style = ParagraphStyle(
        name="AntonymText",
        fontSize=12,
        leading=20,
        leftIndent=15,
        textColor=colors.HexColor("#b71c1c")
    )

    # --- Content generation ---
    for i, word_data in enumerate(word_list):
        word_title = word_data['word'].title()
        elements.append(Paragraph(word_title, title_style))
        elements.append(Spacer(1, 4))

        # ❖ Meanings
        elements.append(Paragraph(
            "<font color='#1a237e'><b>❖ Meanings</b></font>", section_style))

        for meaning_text in word_data["meanings"]:
            definition, examples = parse_meaning_and_examples(meaning_text.strip())
            elements.append(Paragraph(definition, meaning_style))

            if examples:
                bullets = ListFlowable(
                    [
                        ListItem(
                            Paragraph(f"<i>{ex}</i>", example_style),
                            value="→"
                        ) for ex in examples
                    ],
                    bulletType="bullet",
                    bulletFontName="Helvetica",
                    bulletFontSize=10,
                    bulletColor=colors.HexColor("#9e9e9e"),
                    leftIndent=20
                )
                elements.append(bullets)

            elements.append(Spacer(1, 6))

        elements.append(Spacer(1, 10))

        # ✔ Synonyms
        elements.append(Paragraph(
            "<font color='#1b5e20'><b>✔ Synonyms</b></font>", section_style))

        if word_data["synonyms"]:
            for synonym in word_data["synonyms"]:
                elements.append(Paragraph(f"• {synonym}", synonym_style))
        else:
            elements.append(Paragraph("No synonyms provided.", synonym_style))
        elements.append(Spacer(1, 10))

        # ✘ Antonyms
        elements.append(Paragraph(
            "<font color='#b71c1c'><b>✘ Antonyms</b></font>", section_style))

        if word_data["antonyms"]:
            for antonym in word_data["antonyms"]:
                elements.append(Paragraph(f"• {antonym}", antonym_style))
        else:
            elements.append(Paragraph("No antonyms provided.", antonym_style))
        elements.append(Spacer(1, 16))

        # Page break after each word
        if i != len(word_list) - 1:
            elements.append(PageBreak())

    doc.build(elements)
    buffer.seek(0)
    return buffer


# --- Streamlit App Interface ---
st.title("📘 JSON to Beautiful PDF")

uploaded_file = st.file_uploader("Upload your JSON file", type=["json"])

if uploaded_file:
    try:
        word_list = json.load(uploaded_file)
        st.success("✅ JSON loaded successfully.")

        if st.button("📄 Generate PDF"):
            date_str = datetime.now().strftime("%y%m%d")
            pdf_filename = f"{date_str}_styled_words.pdf"
            pdf_bytes = create_combined_pdf(word_list)

            st.download_button(
                label=f"📥 Download PDF ({pdf_filename})",
                data=pdf_bytes,
                file_name=pdf_filename,
                mime="application/pdf"
            )
    except Exception as e:
        st.error(f"❌ Error: {e}")