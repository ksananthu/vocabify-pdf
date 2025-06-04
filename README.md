# 📘 JSON to Styled PDF Generator

This is a **Streamlit web app** that takes a JSON file containing English words with their meanings, synonyms, and antonyms, and compiles them into a **well-formatted PDF**.

---

## ✨ Features

- ✅ Upload a JSON file with word definitions
- ✅ Combines **all words into a single PDF**
- ✅ Each word is a **capitalized, bold H1 title**
- ✅ Sections for **Meanings**, **Synonyms**, and **Antonyms** are bold H3 headers
- ✅ Meanings:
  - Are listed with bullets
  - If they include `=>`, the text after `=>` is moved to a **new line** and rendered in *italics*
- ✅ Adds proper spacing, formatting, and readability
- ✅ Downloads the file with today's date as the filename (e.g., `240604_words.pdf`)
- ✅ **Secure file download** using `BytesIO`

---

## 🖼 Sample Input JSON Format

```json
[
  {
    "word": "advent",
    "meanings": [
      "1. The arrival of something important. => Life changed with the advent of electricity."
    ],
    "synonyms": ["arrival", "beginning"],
    "antonyms": ["departure", "end"]
  },
  {
    "word": "quirk",
    "meanings": [
      "1. A strange habit. => She had a quirk of humming while reading."
    ],
    "synonyms": ["oddity", "peculiarity"],
    "antonyms": ["normality"]
  }
]
