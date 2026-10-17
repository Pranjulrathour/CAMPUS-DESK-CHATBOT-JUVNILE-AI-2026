# Finds the office email, extension, location and office hours on the handbook's contacts page.
import re


def find_office_contact(pages):
    page = next((p for p in pages if re.search(r"contacts", p["title"], re.I)), None)
    page = page or next((p for p in pages if re.search(r"important contacts|office hours", p["text"], re.I)), pages[-1])
    text = page["text"]

    contact = {"office": "Student Affairs Office", "email": None, "phone": None,
               "location": None, "hours": None, "page": page["page"]}

    # Table row: office name, location, email, extension (one per line in the extracted text).
    row = re.search(r"Student Affairs Office\s*\n(.+?)\n(\S+@\S+)\n(\d+)", text)
    if row:
        contact["location"], contact["email"] = row.group(1), row.group(2)
        contact["phone"] = f"Ext. {row.group(3)}"
    else:
        email = re.search(r"\S+@\S+\.\w+", text)
        contact["email"] = email.group(0) if email else None
        phone = re.search(r"(?:phone|tel)\D*(\d[\d\- ]{6,})", text, re.I)
        contact["phone"] = phone.group(1).strip() if phone else None

    hours = re.search(r"Office hours\s*\n(.+?)(?:\nRaising a request|\n[A-Z ]{6,}\?|\Z)", text, re.S)
    if hours:
        sentences = re.split(r"(?<=\.)\s+", " ".join(hours.group(1).split()))
        contact["hours"] = " ".join(sentences[:2])
    return contact
