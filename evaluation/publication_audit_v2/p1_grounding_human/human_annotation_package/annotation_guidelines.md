# Scientific Claim & Citation Human Annotation Guidelines

## 1. Overview
Annotators evaluate generated scientific responses against retrieved candidate passages along two primary dimensions:
1. **Claim Factuality (Entailment)**: Does the candidate passage directly entail the factual claim made in the text?
2. **Citation Accuracy**: Does the specific bracketed citation (e.g., [P01]) correspond to the exact passage supporting the claim?

## 2. Classification Schema
- **SUPPORTED**: The claim is directly stated or strictly entailed by the referenced text chunk.
- **CONTRADICTED**: The retrieved text directly refutes the statement made.
- **UNSUPPORTED / HALLUCINATED**: The statement makes a positive factual assertion that is absent from the referenced context.
- **EPISTEMIC ABSTENTION**: The response acknowledges that the provided literature does not support or address the user query.
