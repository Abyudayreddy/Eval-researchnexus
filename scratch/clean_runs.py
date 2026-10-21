import docx

doc = docx.Document(r"C:\Users\Abyureddy\OneDrive\Desktop\SDC2\SDC Review 1\SRS_V1_ (2).docx")

for p in doc.paragraphs:
    for r in p.runs:
        if "\x00" in r.text or "" in r.text:
            cleaned = r.text.replace("\x00", "").replace("", "")
            r.text = cleaned

doc.save(r"C:\Users\Abyureddy\OneDrive\Desktop\SDC2\SDC Review 1\SRS_V1_ (2).docx")
print("Cleaned character encoding in runs.")
