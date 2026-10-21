import docx

doc = docx.Document(r"C:\Users\Abyureddy\OneDrive\Desktop\SDC2\SDC Review 1\SRS_V1_ (2).docx")

for i, p in enumerate(doc.paragraphs):
    if "\x00" in p.text:
        new_text = p.text.replace("\x00", "")
        p.text = new_text

doc.save(r"C:\Users\Abyureddy\OneDrive\Desktop\SDC2\SDC Review 1\SRS_V1_ (2).docx")
print("Cleaned null bytes.")
