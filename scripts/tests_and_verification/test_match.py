def normalize_term(term):
    term = term.lower()
    if term.endswith('ies'): return term[:-3] + 'y'
    if term.endswith('es') and len(term) > 3: return term[:-2]
    if term.endswith('s') and len(term) > 3: return term[:-1]
    return term

term = "cities"
norm = normalize_term(term)
print(f"Norm: {norm}")

text = "Evaluating smart cities and their approaches."
matched = norm in text
print(f"Matched '{norm}' in text? {matched}")
