Chapter 1: Understanding the Project
Section 1: Problem Statement
A. Understanding the Problem
1.	What is the problem that our project is trying to solve? 
2.	Why do researchers and students find it difficult to analyze research papers manually? 
3.	What challenges do researchers face while searching for relevant information from research papers? 
4.	Why is manual literature review time-consuming? 
5.	What happens when the number of research papers increases every year? 
6.	Why is there a need for an intelligent research paper assistant? 
7.	What are the limitations of manually reading research papers? 
8.	Why is retrieving the correct information from multiple papers difficult? 
9.	How does the increasing volume of scientific literature affect researchers? 
10.	Why is an automated solution required for research paper analysis? 
________________________________________
B. Existing Solution
11.	What solutions are currently available for research paper question answering? 
12.	What is OpenScholar? 
13.	What problem does OpenScholar solve? 
14.	How does OpenScholar help researchers? 
15.	What are the major features of OpenScholar? 
16.	Does OpenScholar answer questions from a single paper or multiple papers? 
17.	What is literature synthesis? 
18.	How is literature synthesis different from document summarization? 
19.	What are the strengths of OpenScholar? 
20.	Why was OpenScholar selected as the base paper for this project? 
________________________________________
C. Limitations of the Existing System
21.	What are the limitations of the existing system? 
22.	Why is explainability important in research assistants? 
23.	Why do users need supporting evidence for generated answers? 
24.	Why is answer reliability important in scientific research? 
25.	Why is retrieval quality important in RAG systems? 
26.	Why may a single retrieval technique not always retrieve the most relevant information? 
27.	Why is updating the knowledge base a challenge in existing systems? 
28.	How can outdated research papers affect the generated answers? 
29.	Why should AI-generated answers be transparent? 
30.	How do these limitations motivate the proposed project? 
________________________________________
D. Proposed Solution
31.	What is the title of the proposed project? 
32.	What is ResearchMind? 
33.	What is the primary objective of ResearchMind? 
34.	How does ResearchMind address the limitations of the existing system? 
35.	What are the major modules of ResearchMind? 
36.	What are the expected inputs to ResearchMind? 
37.	What are the expected outputs of ResearchMind? 
38.	Who are the end users of ResearchMind? 
39.	What are the expected benefits of ResearchMind? 
40.	What makes ResearchMind different from a normal research paper chatbot? 
________________________________________
E. Project Objectives
41.	What are the objectives of ResearchMind? 
42.	Why is Hybrid Retrieval included in the proposed system? 
43.	Why is Section-Aware Retrieval proposed? 
44.	Why is Evidence Highlighting included? 
45.	Why is Groundedness Assessment required? 
46.	Why is Trust Score generation important? 
47.	Why is the Dynamic Research Paper Ingestion Pipeline proposed? 
48.	Why is Explainable AI included in the project? 
49.	How do all the proposed modules improve the existing system? 
50.	Which objective is expected to contribute the most towards improving the research assistant? 
________________________________________
F. Project Scope
51.	What is the scope of the proposed project? 
52.	Which type of research papers will the system support? 
53.	Can the system work with research papers from different domains? 
54.	What are the limitations of the proposed project? 
55.	Does the project generate new research papers? 
56.	Does the project replace human researchers? 
57.	Can the project be extended to other domains? 
58.	Can users upload their own research papers? 
59.	Can the knowledge base be updated after deployment? 
60.	What future enhancements can be added to the project? 
________________________________________
G. Project Justification
61.	Why is this project relevant in today's research environment? 
62.	Why is ResearchMind useful for students? 
63.	Why is ResearchMind useful for researchers? 
64.	How can ResearchMind improve the literature review process? 
65.	How can ResearchMind save researchers' time? 
66.	Why is evidence-supported answer generation important? 
67.	Why should users trust AI-generated answers? 
68.	How does ResearchMind improve answer transparency? 
69.	How does ResearchMind improve answer reliability? 
70.	Why do you believe ResearchMind is a useful research project? 
________________________________________
H. Management Questions
71.	What exactly is the problem you are solving? 
72.	Why is this problem important? 
73.	How did you identify this problem? 
74.	Why did you choose this project? 
75.	Why did you select OpenScholar as the base paper? 
76.	What improvements are you proposing over the base paper? 
77.	If OpenScholar already works well, why is ResearchMind needed? 
78.	What is the novelty in your proposed project? 
79.	How will you prove that your proposed system is better? 
80.	What is the expected impact of your project? 

MODULE 1 – PROJECT FOUNDATION
Chapter 2 – Base Paper (OpenScholar)
________________________________________
Section 1 – Introduction to OpenScholar
Understanding
1.	What is OpenScholar? 
2.	Why was OpenScholar developed? 
3.	What problem does OpenScholar solve? 
4.	Which domain does OpenScholar belong to? 
5.	Who developed OpenScholar? 
6.	Where was OpenScholar published? 
7.	What is the title of the base paper? 
8.	Why did we choose OpenScholar as the base paper? 
9.	What makes OpenScholar different from a normal chatbot? 
10.	What are the main objectives of OpenScholar? 
________________________________________
Existing Problem
11.	What problem existed before OpenScholar? 
12.	Why were traditional search engines not sufficient? 
13.	Why can't ChatGPT alone answer research questions accurately? 
14.	What happens when an LLM answers without retrieval? 
15.	Why is literature synthesis difficult? 
16.	Why do researchers spend a lot of time reading papers? 
17.	Why do existing RAG systems struggle with scientific literature? 
18.	What challenges are involved in answering questions from multiple research papers? 
19.	Why is citation-supported answering important? 
20.	How does OpenScholar solve these problems? 
________________________________________
Section 2 – OpenScholar Architecture
21.	Draw the complete architecture of OpenScholar. 
22.	Explain the OpenScholar workflow. 
23.	What are the major modules in OpenScholar? 
24.	What is the first step in the OpenScholar pipeline? 
25.	What is the last step in the OpenScholar pipeline? 
26.	Which modules perform retrieval? 
27.	Which module performs reranking? 
28.	Which module generates the final answer? 
29.	Which module stores the research papers? 
30.	Explain the complete data flow in OpenScholar. 
________________________________________
Section 3 – OpenScholar Data Store (OSDS)
31.	What is OSDS? 
32.	Why is OSDS required? 
33.	What does OSDS contain? 
34.	Approximately how many research papers are available in OSDS? 
35.	Up to which year does OSDS contain research papers? 
36.	How were the papers collected? 
37.	Why is OSDS considered a knowledge base? 
38.	How are research papers stored inside OSDS? 
39.	What happens before storing research papers? 
40.	Why is preprocessing required before storage? 
________________________________________
Understanding OSDS
41.	Can OSDS be updated? 
42.	Is OSDS static or dynamic? 
43.	What types of research papers are included? 
44.	Does OSDS contain only Computer Science papers? 
45.	Can duplicate papers exist in OSDS? 
46.	What happens if new papers are published? 
47.	Why is maintaining such a large datastore difficult? 
48.	Can students recreate OSDS? 
49.	Why are we not using the complete OSDS? 
50.	What dataset will ResearchMind use instead? 
________________________________________
Section 4 – Retrieval
51.	What is retrieval? 
52.	Why is retrieval required? 
53.	At which stage is retrieval performed? 
54.	What is retrieved? 
55.	Does retrieval retrieve papers or passages? 
56.	Why are passages retrieved instead of complete papers? 
57.	What is the input to the retriever? 
58.	What is the output of the retriever? 
59.	Which retriever is used in OpenScholar? 
60.	Why did OpenScholar choose Dense Retrieval? 
________________________________________
Bi-Encoder Retriever
61.	What is a Bi-Encoder Retriever? 
62.	Why is it called a Bi-Encoder? 
63.	How does the Bi-Encoder work? 
64.	How does it understand relevance? 
65.	Is the Bi-Encoder trained? 
66.	On what data is it trained? 
67.	What are embeddings? 
68.	How are query embeddings generated? 
69.	How are document embeddings generated? 
70.	How are similar passages identified? 
71.	Which similarity measure is generally used? 
72.	Why is the Bi-Encoder considered fast? 
73.	What are the advantages of a Bi-Encoder? 
74.	What are its limitations? 
75.	Why can't a Bi-Encoder directly generate answers? 
________________________________________
Section 5 – Reranking
76.	Why is reranking required? 
77.	What happens if reranking is removed? 
78.	Which reranker is used in OpenScholar? 
79.	What is a Cross-Encoder? 
80.	Why is it called a Cross-Encoder? 
81.	How does the Cross-Encoder work? 
82.	What is the input to the Cross-Encoder? 
83.	What is the output of the Cross-Encoder? 
84.	How does the Cross-Encoder score relevance? 
85.	Why is the Cross-Encoder more accurate than the Bi-Encoder? 
86.	Why is the Cross-Encoder slower? 
87.	Why is it used only after retrieval? 
88.	How many retrieved passages are reranked? 
89.	How many top passages are finally selected? 
90.	What happens after reranking? 
________________________________________
Section 6 – Large Language Model
91.	Which Large Language Model is used? 
92.	Why is an LLM required? 
93.	What is the role of the LLM? 
94.	Does the LLM retrieve information? 
95.	What is the input given to the LLM? 
96.	What is the output generated by the LLM? 
97.	Why is retrieved context provided to the LLM? 
98.	Can the LLM answer without retrieval? 
99.	What happens if the retrieved context is wrong? 
100.	Why is retrieval quality important for the LLM? 
________________________________________
Section 7 – ScholarQABench
101.	What is ScholarQABench? 
102.	Why was ScholarQABench created? 
103.	Who created ScholarQABench? 
104.	What is the purpose of ScholarQABench? 
105.	Is ScholarQABench a training dataset or an evaluation benchmark? 
106.	How was ScholarQABench created? 
107.	Which existing datasets were used? 
108.	Which domains are covered? 
109.	What types of questions are included? 
110.	Does it contain expert-written questions? 
111.	Does it contain expert-written answers? 
112.	Why is expert evaluation important? 
113.	How is OpenScholar evaluated using ScholarQABench? 
114.	Why can't students directly create a benchmark like ScholarQABench? 
115.	Will ResearchMind use ScholarQABench? 
________________________________________
Section 8 – Evaluation
116.	How was OpenScholar evaluated? 
117.	Which evaluation metrics were used? 
118.	What does Faithfulness measure? 
119.	What does Groundedness measure? 
120.	What does Answer Correctness measure? 
121.	What is Citation Accuracy? 
122.	Why is evaluation necessary? 
123.	How do we know OpenScholar performs better? 
124.	What is a baseline model? 
125.	Why should ResearchMind compare against OpenScholar? 
________________________________________
Section 9 – Limitations
126.	What are the limitations of OpenScholar? 
127.	Why does OpenScholar not provide Evidence Highlighting? 
128.	Why doesn't it generate a Trust Score? 
129.	Why is explainability limited? 
130.	Why is retrieval still challenging? 
131.	Why is maintaining OSDS difficult? 
132.	Why isn't the knowledge base updated automatically? 
133.	Why is OpenScholar difficult for undergraduate implementation? 
134.	Which limitations are addressed by ResearchMind? 
135.	Which limitations remain unsolved? 
________________________________________
Section 10 – ResearchMind Perspective
136.	Which OpenScholar modules are reused in ResearchMind? 
137.	Which modules are modified? 
138.	Which modules are newly proposed? 
139.	Why are we using Hybrid Retrieval instead of only Dense Retrieval? 
140.	Why are we introducing Section-Aware Retrieval? 
141.	Why is Evidence Highlighting proposed? 
142.	Why is Groundedness Assessment proposed? 
143.	Why is Trust Score Generation proposed? 
144.	Why is Dynamic Research Paper Ingestion proposed? 
145.	Which module contributes the maximum novelty? 
________________________________________
Section 11 – Management Questions
146.	Why did you select OpenScholar instead of PaperQA? 
147.	Why is OpenScholar a better base paper? 
148.	If OpenScholar already works well, why is ResearchMind required? 
149.	What is the biggest contribution of OpenScholar? 
150.	What is the biggest limitation of OpenScholar? 
151.	How will you prove that ResearchMind is better? 
152.	If OpenScholar releases a new version, how will your project change? 
153.	Can ResearchMind completely replace OpenScholar? 
154.	If OpenScholar becomes open source with all its resources, will your project still be useful? 
155.	If you were one of the OpenScholar authors, what improvement would you add in the next version?

MODULE 2 – DATASET & KNOWLEDGE BASE
Chapter 3 – Dataset
________________________________________
Section 1 – Dataset Fundamentals
Understanding
1.	What is a dataset? 
2.	Why is a dataset required? 
3.	Where are datasets used? 
4.	Why are datasets important in Artificial Intelligence? 
5.	Why are datasets important in Machine Learning? 
6.	Why are datasets important in Retrieval-Augmented Generation (RAG)? 
7.	What types of datasets are used in AI projects? 
8.	What is the difference between structured and unstructured datasets? 
9.	Is a research paper collection considered a dataset? 
10.	Why are research papers used as the dataset in our project? 
________________________________________
Section 2 – Our Dataset
11.	Which dataset will ResearchMind use? 
12.	Why are we not using the complete OpenScholar dataset? 
13.	How many research papers will initially be collected? 
14.	Which research domain will the dataset cover? 
15.	Why are we selecting domain-specific research papers? 
16.	From where will the research papers be collected? 
17.	Which websites provide open-access research papers? 
18.	Why should we use only open-access research papers? 
19.	What file format will be used for storing the research papers? 
20.	Why are PDFs preferred? 
________________________________________
Section 3 – Dataset Collection
21.	How will students collect research papers? 
22.	What criteria should be followed while selecting research papers? 
23.	How can duplicate papers be identified? 
24.	Should very old research papers be included? 
25.	Should survey papers be included? 
26.	Should review papers be included? 
27.	Should conference papers and journal papers both be used? 
28.	How many papers are sufficient for the initial implementation? 
29.	Can the dataset be expanded later? 
30.	Why should the dataset be carefully curated? 
________________________________________
Section 4 – Dataset Organization
31.	How should the collected papers be organized? 
32.	Should papers be grouped by domain? 
33.	Should papers be grouped by year? 
34.	Should papers be grouped by topic? 
35.	What folder structure should be followed? 
36.	Why is proper dataset organization important? 
37.	Can multiple versions of the same paper exist? 
38.	How should duplicate versions be handled? 
39.	How should revised editions be managed? 
40.	How should deleted papers be handled? 
________________________________________
Section 5 – Metadata
41.	What is metadata? 
42.	Why is metadata required? 
43.	What metadata should be extracted from each research paper? 
44.	Why is the title stored? 
45.	Why are authors stored? 
46.	Why is the publication year stored? 
47.	Why are keywords stored? 
48.	Why is the abstract useful? 
49.	Why is DOI important? 
50.	Where will metadata be stored? 
________________________________________
Metadata Usage
51.	How does metadata improve retrieval? 
52.	Can metadata be used for filtering? 
53.	Can metadata improve search accuracy? 
54.	Can metadata be used during reranking? 
55.	Can metadata help generate citations? 
56.	Can metadata help identify duplicate papers? 
57.	Can metadata support future enhancements? 
58.	What happens if metadata is missing? 
59.	Can the project work without metadata? 
60.	Why is metadata considered valuable information? 
________________________________________
Section 6 – Dataset Preprocessing
61.	Why is preprocessing required? 
62.	What preprocessing steps are performed? 
63.	Why should unwanted text be removed? 
64.	Why should empty pages be ignored? 
65.	How are corrupted PDFs handled? 
66.	How are scanned PDFs handled? 
67.	How are image-only PDFs processed? 
68.	How are special symbols handled? 
69.	How are tables handled? 
70.	How are references handled during preprocessing? 
________________________________________
Section 7 – Dataset Quality
71.	What makes a good dataset? 
72.	Why should irrelevant papers be removed? 
73.	Why should duplicate papers be removed? 
74.	How can dataset quality be verified? 
75.	What problems occur due to poor-quality datasets? 
76.	How does dataset quality affect retrieval? 
77.	How does dataset quality affect answer generation? 
78.	How does dataset quality affect evaluation? 
79.	Can poor datasets increase hallucinations? 
80.	Why is dataset quality more important than dataset size? 
________________________________________
Section 8 – Knowledge Base
81.	What is a knowledge base? 
82.	How is a knowledge base different from a dataset? 
83.	How does a dataset become a knowledge base? 
84.	At which stage is the knowledge base created? 
85.	What information is stored in the knowledge base? 
86.	Why is the knowledge base required? 
87.	Can the knowledge base be updated? 
88.	Can the knowledge base be deleted and recreated? 
89.	What happens if the knowledge base is corrupted? 
90.	Does the knowledge base store complete research papers or processed information? 
________________________________________
Section 9 – Dynamic Dataset Updates
91.	What is Dynamic Research Paper Ingestion? 
92.	Why is dynamic ingestion required? 
93.	How will newly published papers be identified? 
94.	Which online repositories can be monitored? 
95.	How will new research papers be downloaded? 
96.	How will duplicate papers be avoided? 
97.	What happens after a new paper is downloaded? 
98.	Why is retraining the LLM not required? 
99.	How is the vector database updated? 
100.	How does this make the system dynamic? 
________________________________________
Section 10 – Project Perspective
101.	Why did we select a domain-specific dataset? 
102.	Why are we using PDFs instead of plain text files? 
103.	Why are we storing metadata? 
104.	Why do we create a knowledge base? 
105.	Why is preprocessing necessary before chunking? 
106.	Why is dynamic ingestion included in our project? 
107.	Can students build this dataset themselves? 
108.	What challenges may arise while creating the dataset? 
109.	How does the dataset affect the overall performance of ResearchMind? 
110.	Which future improvements can be made to the dataset? 
________________________________________
Section 11 – Management Questions
111.	Why did you choose only 200–300 research papers instead of 40 million? 
112.	Why not use the complete OpenScholar dataset? 
113.	How will you prove your dataset is sufficient? 
114.	What if new research papers are published tomorrow? 
115.	How will your system include newly published papers? 
116.	What if duplicate papers exist in your dataset? 
117.	Can your dataset be reused for another project? 
118.	If your dataset doubles in size, what changes are required? 
119.	How will you ensure dataset quality? 
120.	What is the difference between the dataset and the knowledge base?

MODULE 3 – DOCUMENT PROCESSING
Chapter 4 – PDF Processing & Text Extraction
________________________________________
Section 1 – Introduction to PDF Processing
Understanding
1.	What is PDF processing? 
2.	Why is PDF processing required in ResearchMind? 
3.	Why are research papers usually available in PDF format? 
4.	Why can't we directly use PDF files in a RAG system? 
5.	What is the objective of PDF processing? 
6.	At which stage of the ResearchMind pipeline is PDF processing performed? 
7.	What is the input to the PDF processing module? 
8.	What is the output of the PDF processing module? 
9.	What happens after PDF processing? 
10.	Can the project work without PDF processing? 
________________________________________
Section 2 – PDF Format
11.	What is a PDF? 
12.	What are the characteristics of a PDF document? 
13.	Why are PDFs preferred for research papers? 
14.	What types of content can a PDF contain? 
15.	Does a PDF always contain selectable text? 
16.	What is the difference between a text-based PDF and a scanned PDF? 
17.	How can we identify whether a PDF is text-based or scanned? 
18.	Can two PDFs have different internal structures? 
19.	Why is extracting information from PDFs challenging? 
20.	What problems may occur while reading PDF files? 
________________________________________
Section 3 – Text Extraction
21.	What is text extraction? 
22.	Why is text extraction required? 
23.	How is text extracted from a research paper? 
24.	What is the input to the text extraction process? 
25.	What is the output of text extraction? 
26.	What types of information are extracted? 
27.	Is the extracted text always clean? 
28.	What information is ignored during text extraction? 
29.	Can images be converted into text during extraction? 
30.	What happens if text extraction fails? 
________________________________________
Section 4 – PyMuPDF
31.	What is PyMuPDF? 
32.	Why are we using PyMuPDF? 
33.	Where is PyMuPDF used in our project? 
34.	Which programming language supports PyMuPDF? 
35.	Is PyMuPDF an open-source library? 
36.	What can PyMuPDF extract from a PDF? 
37.	Can PyMuPDF extract images? 
38.	Can PyMuPDF extract tables? 
39.	Can PyMuPDF extract metadata? 
40.	Why is PyMuPDF suitable for research paper processing? 
________________________________________
Implementation
41.	How is PyMuPDF installed? 
42.	Which Python package is used? 
43.	How do we open a PDF using PyMuPDF? 
44.	How do we read pages from a PDF? 
45.	How do we extract text from each page? 
46.	How do we process multiple PDFs? 
47.	How is the extracted text stored? 
48.	How are errors handled while reading PDFs? 
49.	Can PyMuPDF process very large PDF files? 
50.	What precautions should be taken while using PyMuPDF? 
________________________________________
Section 5 – Why PyMuPDF?
51.	Why did we choose PyMuPDF? 
52.	Why not PyPDF2? 
53.	Why not PDFPlumber? 
54.	Why not Apache Tika? 
55.	What are the advantages of PyMuPDF? 
56.	What are the limitations of PyMuPDF? 
57.	Which library extracts text faster? 
58.	Which library preserves formatting better? 
59.	Which library is easier for students? 
60.	Which library is more suitable for ResearchMind? 
________________________________________
Section 6 – OCR
61.	What is OCR? 
62.	What does OCR stand for? 
63.	Why is OCR required? 
64.	When should OCR be used? 
65.	Is OCR required for every PDF? 
66.	Which OCR library is commonly used in Python? 
67.	What is Tesseract OCR? 
68.	What is EasyOCR? 
69.	Can OCR recognize handwritten text? 
70.	What are the limitations of OCR? 
________________________________________
OCR vs Text Extraction
71.	What is the difference between OCR and text extraction? 
72.	When should text extraction be preferred? 
73.	When should OCR be preferred? 
74.	Can OCR reduce processing speed? 
75.	Can OCR introduce errors? 
76.	How does OCR affect accuracy? 
77.	Can scanned research papers be processed without OCR? 
78.	What happens if OCR is skipped for scanned PDFs? 
79.	Can OCR preserve formatting? 
80.	Which approach will ResearchMind use? 
________________________________________
Section 7 – Research Paper Content
81.	Which parts of a research paper should be extracted? 
82.	Should the title be extracted? 
83.	Should the abstract be extracted? 
84.	Should the methodology be extracted? 
85.	Should references be extracted? 
86.	Should figures be extracted? 
87.	Should tables be extracted? 
88.	Should equations be extracted? 
89.	Should captions be extracted? 
90.	Should acknowledgements be extracted? 
________________________________________
Section 8 – Challenges
91.	What challenges are faced during PDF processing? 
92.	How are corrupted PDFs handled? 
93.	How are encrypted PDFs handled? 
94.	How are password-protected PDFs handled? 
95.	What happens if pages are missing? 
96.	What happens if text overlaps? 
97.	How are multi-column research papers handled? 
98.	How are headers and footers handled? 
99.	Why should unnecessary text be removed? 
100.	How does poor text extraction affect the project? 
________________________________________
Section 9 – Project Perspective
101.	Why is PDF processing the first implementation step? 
102.	Why can't chunking be performed directly on a PDF? 
103.	Why is clean text required before chunking? 
104.	Why should text extraction be accurate? 
105.	How does PDF quality affect embeddings? 
106.	How does PDF quality affect retrieval? 
107.	How does PDF quality affect answer generation? 
108.	Can ResearchMind process research papers from different publishers? 
109.	Can ResearchMind process scanned research papers? 
110.	What improvements can be added to the PDF processing module? 
________________________________________
Section 10 – Management Questions
111.	Why did you choose PyMuPDF? 
112.	Why not PDFPlumber? 
113.	Can PyMuPDF process all research papers? 
114.	What happens if a PDF contains only images? 
115.	Why is OCR not used for every PDF? 
116.	How will your system process 5,000 research papers? 
117.	What if text extraction produces incorrect text? 
118.	How will you verify the extracted text? 
119.	How does PDF processing affect the overall system performance? 
120.	If you redesign this module, what improvements would you make?

MODULE 3 – DOCUMENT PROCESSING
Chapter 5 – Document Structure Extraction & Section-Aware Retrieval
________________________________________
Section 1 – Document Structure
Understanding
1.	What is document structure? 
2.	Why do research papers have a predefined structure? 
3.	Why is understanding the document structure important? 
4.	What are the common sections in a research paper? 
5.	Why are research papers divided into sections? 
6.	Is the document structure the same for every research paper? 
7.	Which sections are usually present in IEEE research papers? 
8.	Which sections are mandatory in most research papers? 
9.	What is the purpose of dividing a research paper into sections? 
10.	How does document structure improve readability? 
________________________________________
Section 2 – Research Paper Sections
11.	What is the Title section? 
12.	What information does the Title provide? 
13.	What is an Abstract? 
14.	Why is the Abstract important? 
15.	What information is available in the Introduction? 
16.	What is Literature Review (Related Work)? 
17.	What information is available in the Methodology section? 
18.	What information is available in the Experimental Results section? 
19.	What information is available in the Conclusion? 
20.	Why are References included? 
________________________________________
Section 3 – Document Structure Extraction
21.	What is Document Structure Extraction? 
22.	Why is Document Structure Extraction required? 
23.	At which stage of the ResearchMind pipeline is it performed? 
24.	What is the input to Document Structure Extraction? 
25.	What is the output of this module? 
26.	What happens before Document Structure Extraction? 
27.	What happens after Document Structure Extraction? 
28.	Is this module available in traditional RAG systems? 
29.	Why did we include this module in ResearchMind? 
30.	Can ResearchMind work without Document Structure Extraction? 
________________________________________
Section 4 – Section Detection
31.	What is Section Detection? 
32.	How are section headings identified? 
33.	Can section headings be extracted automatically? 
34.	Which libraries can help detect headings? 
35.	How do we identify the Abstract section? 
36.	How do we identify the Introduction section? 
37.	How do we identify the Methodology section? 
38.	How do we identify the Results section? 
39.	How do we identify the Conclusion section? 
40.	What happens if a paper follows a different section naming convention? 
________________________________________
Section 5 – Metadata Generation
41.	What metadata is generated after section detection? 
42.	Why is section information stored as metadata? 
43.	How is section metadata associated with text chunks? 
44.	Can one chunk belong to multiple sections? 
45.	How is the section name stored? 
46.	Why is section metadata important for retrieval? 
47.	Can metadata be updated later? 
48.	How does metadata improve search? 
49.	What happens if metadata is incorrect? 
50.	Can the project work without section metadata? 
________________________________________
Section 6 – Section-Aware Retrieval
51.	What is Section-Aware Retrieval? 
52.	Why is Section-Aware Retrieval required? 
53.	What problem does it solve? 
54.	How is Section-Aware Retrieval different from normal retrieval? 
55.	At which stage is Section-Aware Retrieval performed? 
56.	Which module uses section metadata? 
57.	Is Section-Aware Retrieval one of the novelties of ResearchMind? 
58.	Why is it considered an enhancement? 
59.	Can Section-Aware Retrieval improve answer quality? 
60.	Can it reduce irrelevant retrieval? 
________________________________________
Section 7 – Internal Working
61.	How does Section-Aware Retrieval work? 
62.	What is the input to Section-Aware Retrieval? 
63.	What is the output? 
64.	How does the system decide which section is important? 
65.	Does the user need to mention the section name? 
66.	Can the system automatically identify the relevant section? 
67.	How are chunks filtered based on sections? 
68.	What happens after section filtering? 
69.	Does BM25 use section information? 
70.	Does Dense Retrieval use section information? 
________________________________________
Section 8 – Query Examples
71.	If the user asks "What methodology was used?", which section should be searched first? 
72.	If the user asks "What are the results?", which section should be searched? 
73.	If the user asks "What are the future research directions?", which section should be searched? 
74.	If the user asks "What problem does this paper solve?", which section should be searched? 
75.	If the user asks "Summarize this paper.", should only one section be retrieved? 
76.	Which sections are useful for comparing two research papers? 
77.	Which section usually contains the research gap? 
78.	Which section usually contains evaluation metrics? 
79.	Which section usually contains datasets used? 
80.	Can one query require information from multiple sections? 
________________________________________
Section 9 – Advantages
81.	What are the advantages of Document Structure Extraction? 
82.	What are the advantages of Section-Aware Retrieval? 
83.	How does it improve retrieval accuracy? 
84.	How does it reduce unnecessary retrieval? 
85.	How does it improve answer quality? 
86.	How does it reduce hallucination? 
87.	How does it improve context relevance? 
88.	Why is it useful for research papers? 
89.	Can it reduce processing time? 
90.	How does it improve user experience? 
________________________________________
Section 10 – Limitations
91.	What are the limitations of Section-Aware Retrieval? 
92.	What happens if section headings are missing? 
93.	What happens if section names differ across publishers? 
94.	Can incorrect section detection affect retrieval? 
95.	Can all research papers be processed correctly? 
96.	How are unusual document structures handled? 
97.	Can scanned PDFs create problems? 
98.	How can incorrect metadata affect answer generation? 
99.	Can this module fail? 
100.	How can these limitations be reduced? 
________________________________________
Section 11 – Comparisons
101.	Normal Retrieval vs Section-Aware Retrieval 
102.	Keyword Search vs Section-Aware Retrieval 
103.	Dense Retrieval vs Section-Aware Retrieval 
104.	Hybrid Retrieval vs Section-Aware Retrieval 
105.	Does Section-Aware Retrieval replace Hybrid Retrieval? 
106.	Can both work together? 
107.	Which module runs first? 
108.	Why is Section-Aware Retrieval not a replacement for reranking? 
109.	Why is Section-Aware Retrieval considered an enhancement rather than a retrieval algorithm? 
110.	Where exactly does it fit in the ResearchMind architecture? 
________________________________________
Section 12 – Project Perspective
111.	Why did we introduce Document Structure Extraction? 
112.	Why didn't OpenScholar explicitly use Section-Aware Retrieval? 
113.	Why is this considered one of our novelties? 
114.	How does this module integrate with Hybrid Retrieval? 
115.	How does it improve Explainable AI? 
116.	How does it improve Evidence Highlighting? 
117.	How does it improve Groundedness Assessment? 
118.	Does it improve Trust Score generation? 
119.	Which future improvements can be added to this module? 
120.	If this module is removed, how will the overall system be affected? 
________________________________________
Section 13 – Management Questions
121.	Why did you introduce Section-Aware Retrieval? 
122.	Why isn't Dense Retrieval alone sufficient? 
123.	Why doesn't OpenScholar explicitly perform Section-Aware Retrieval? 
124.	How do you know this module improves performance? 
125.	What if the section heading is incorrect? 
126.	Can this module work for books or reports? 
127.	Can it work for documents without headings? 
128.	Is this a retrieval technique or a preprocessing technique? 
129.	How will you evaluate the effectiveness of this module? 
130.	Is Section-Aware Retrieval your novelty or an existing technique adapted to your project?

MODULE 3 – DOCUMENT PROCESSING
Chapter 6 – Text Chunking
________________________________________
Section 1 – Introduction to Chunking
Understanding
1.	What is text chunking? 
2.	Why is chunking required in RAG? 
3.	At which stage of the ResearchMind pipeline is chunking performed? 
4.	What is the input to the chunking process? 
5.	What is the output of chunking? 
6.	Why can't complete research papers be directly converted into embeddings? 
7.	Why can't complete research papers be directly given to the LLM? 
8.	Why is chunking considered an important preprocessing step? 
9.	Can the project work without chunking? 
10.	What happens after chunking? 
________________________________________
Section 2 – Need for Chunking
11.	Why do Large Language Models have context length limitations? 
12.	What is a context window? 
13.	How does chunking solve the context window problem? 
14.	Why is retrieving small chunks better than retrieving complete documents? 
15.	Why is chunking important for semantic search? 
16.	Why is chunking important for retrieval accuracy? 
17.	Why does chunking improve answer quality? 
18.	How does chunking improve retrieval speed? 
19.	How does chunking reduce computational cost? 
20.	How does chunking improve the overall RAG pipeline? 
________________________________________
Section 3 – Chunk Creation
21.	How are chunks created? 
22.	Which module performs chunking? 
23.	Does chunking occur before or after embedding generation? 
24.	Does chunking occur before or after document structure extraction? 
25.	Can one research paper produce multiple chunks? 
26.	Can one section produce multiple chunks? 
27.	Can one chunk contain multiple paragraphs? 
28.	Should a chunk end in the middle of a sentence? 
29.	What happens if a sentence is split incorrectly? 
30.	How do we maintain logical continuity while creating chunks? 
________________________________________
Section 4 – Types of Chunking
31.	What are the different types of chunking? 
32.	What is Fixed-Size Chunking? 
33.	What is Sentence-Based Chunking? 
34.	What is Paragraph-Based Chunking? 
35.	What is Recursive Chunking? 
36.	What is Semantic Chunking? 
37.	What is Token-Based Chunking? 
38.	Which chunking technique is most commonly used in RAG? 
39.	Which chunking technique is easiest to implement? 
40.	Which chunking technique produces better retrieval quality? 
________________________________________
Section 5 – Recursive Character Text Splitter
41.	What is Recursive Character Text Splitter? 
42.	Which library provides Recursive Character Text Splitter? 
43.	Why are we using Recursive Character Text Splitter? 
44.	How does Recursive Character Text Splitter work? 
45.	What separators does it use? 
46.	How does it preserve sentence boundaries? 
47.	Why is Recursive Character Text Splitter suitable for research papers? 
48.	Can Recursive Character Text Splitter split large documents efficiently? 
49.	What are its advantages? 
50.	What are its limitations? 
________________________________________
Section 6 – Chunk Size
51.	What is chunk size? 
52.	How is chunk size measured? 
53.	Why is chunk size important? 
54.	How do we decide the chunk size? 
55.	What factors influence chunk size? 
56.	What happens if the chunk size is too small? 
57.	What happens if the chunk size is too large? 
58.	Why can't one chunk contain an entire research paper? 
59.	Can different documents use different chunk sizes? 
60.	Is there a universally best chunk size? 
________________________________________
Section 7 – Chunk Overlap
61.	What is chunk overlap? 
62.	Why is chunk overlap required? 
63.	How is overlap created? 
64.	What happens if overlap is not used? 
65.	How much overlap should be maintained? 
66.	Can too much overlap reduce performance? 
67.	Can too little overlap affect retrieval? 
68.	How does overlap preserve context? 
69.	How does overlap improve answer quality? 
70.	Does overlap increase storage requirements? 
________________________________________
Section 8 – Metadata and Chunks
71.	What metadata is attached to each chunk? 
72.	Why should each chunk store the paper title? 
73.	Why should each chunk store the section name? 
74.	Why should each chunk store the page number? 
75.	Why should each chunk store document identifiers? 
76.	How does metadata improve retrieval? 
77.	Can metadata improve evidence highlighting? 
78.	Can metadata help generate citations? 
79.	What happens if metadata is missing? 
80.	Why is metadata important for Section-Aware Retrieval? 
________________________________________
Section 9 – Chunk Storage
81.	Where are chunks stored? 
82.	Are chunks stored before or after embedding generation? 
83.	Can chunks be modified later? 
84.	Can duplicate chunks exist? 
85.	How are duplicate chunks identified? 
86.	Can chunks be deleted? 
87.	Can new chunks be added? 
88.	What happens if chunk storage fails? 
89.	Does every chunk generate one embedding? 
90.	How many chunks are typically created from one research paper? 
________________________________________
Section 10 – Project Perspective
91.	Which chunking technique are we using in ResearchMind? 
92.	Why did we choose Recursive Character Text Splitter? 
93.	Why not Fixed-Size Chunking? 
94.	Why not Semantic Chunking for the initial implementation? 
95.	How does chunking support Section-Aware Retrieval? 
96.	How does chunking support Hybrid Retrieval? 
97.	How does chunking improve Evidence Highlighting? 
98.	How does chunking improve Groundedness Assessment? 
99.	How does chunking improve Trust Score generation? 
100.	Which later modules depend on correctly generated chunks? 
________________________________________
Section 11 – Comparisons
101.	Fixed-Size Chunking vs Recursive Chunking 
102.	Recursive Chunking vs Semantic Chunking 
103.	Sentence-Based Chunking vs Paragraph-Based Chunking 
104.	Character-Based Chunking vs Token-Based Chunking 
105.	Small Chunks vs Large Chunks 
106.	Chunking with Overlap vs Without Overlap 
107.	Which chunking method is best for research papers? 
108.	Which chunking method is computationally efficient? 
109.	Which chunking method provides better retrieval quality? 
110.	Which chunking method is most suitable for undergraduate implementation? 
________________________________________
Section 12 – Limitations
111.	What are the limitations of chunking? 
112.	Can chunking break the meaning of a paragraph? 
113.	Can incorrect chunking affect retrieval accuracy? 
114.	Can chunking increase storage requirements? 
115.	Can poor chunking increase hallucinations? 
116.	How can chunking affect embedding quality? 
117.	Can chunking affect reranking? 
118.	How can chunking affect answer generation? 
119.	What improvements can be made to chunking? 
120.	Is chunking still an active research area? 
________________________________________
Section 13 – Management Questions
121.	Why is chunking necessary? 
122.	Why not store the complete research paper as one embedding? 
123.	How did you choose the chunk size? 
124.	Why did you choose the overlap size? 
125.	Why did you choose Recursive Character Text Splitter? 
126.	What happens if chunk overlap is removed? 
127.	Can different chunk sizes be used for different sections? 
128.	How many chunks are generated from one research paper? 
129.	If you double the chunk size, how will the system be affected? 
130.	If you redesign the chunking module, what improvements would you make?

MODULE 4 – REPRESENTING TEXT AS VECTORS
Chapter 7 – Embeddings
________________________________________
Section 1 – Introduction to Embeddings
Understanding
1.	What are embeddings? 
2.	Why are embeddings required in AI applications? 
3.	Why are embeddings important in Retrieval-Augmented Generation (RAG)? 
4.	At which stage of the ResearchMind pipeline are embeddings generated? 
5.	What is the input to the embedding model? 
6.	What is the output of the embedding model? 
7.	Why can't a computer understand plain text directly? 
8.	Why are words converted into numbers? 
9.	What is a vector? 
10.	How are embeddings different from ordinary numbers? 
________________________________________
Section 2 – Need for Embeddings
11.	Why do we need embeddings? 
12.	How do embeddings help computers understand text? 
13.	Why are embeddings used instead of keyword matching? 
14.	How do embeddings capture semantic meaning? 
15.	Why are embeddings important for semantic search? 
16.	How do embeddings improve document retrieval? 
17.	How do embeddings improve question answering? 
18.	How do embeddings improve retrieval accuracy? 
19.	Can a RAG system work without embeddings? 
20.	What happens if embeddings are incorrect? 
________________________________________
Section 3 – Embedding Generation
21.	How are embeddings generated? 
22.	Which model generates embeddings in our project? 
23.	Does every chunk generate one embedding? 
24.	Are embeddings generated before or after chunking? 
25.	Are embeddings generated before or after metadata creation? 
26.	Can one document generate multiple embeddings? 
27.	Are query embeddings generated differently from document embeddings? 
28.	When are query embeddings generated? 
29.	Can embeddings be regenerated? 
30.	What happens after embeddings are generated? 
________________________________________
Section 4 – Embedding Models
31.	What is an embedding model? 
32.	Which embedding model are we using in ResearchMind? 
33.	Why did we choose the BGE embedding model? 
34.	What are BGE embeddings? 
35.	Who developed the BGE embedding model? 
36.	Are BGE embeddings open source? 
37.	Which Python library provides BGE embeddings? 
38.	What are the advantages of BGE embeddings? 
39.	What are the limitations of BGE embeddings? 
40.	Can another embedding model be used? 
________________________________________
Section 5 – Vector Representation
41.	What is a vector? 
42.	How is text converted into a vector? 
43.	What does each value in a vector represent? 
44.	What is the dimensionality of an embedding? 
45.	Why are embeddings high-dimensional vectors? 
46.	Can humans understand embedding values directly? 
47.	Why do similar sentences produce similar vectors? 
48.	Why do unrelated sentences produce different vectors? 
49.	Can identical sentences have identical embeddings? 
50.	How are vectors stored? 
________________________________________
Section 6 – Similarity Measurement
51.	Why do we compare vectors? 
52.	How are two embeddings compared? 
53.	What is similarity search? 
54.	What is cosine similarity? 
55.	Why is cosine similarity commonly used? 
56.	What is dot product similarity? 
57.	What is Euclidean distance? 
58.	Which similarity measure are we using? 
59.	Why was this similarity measure selected? 
60.	How does similarity affect retrieval? 
________________________________________
Section 7 – Practical Implementation
61.	Which Python library generates embeddings? 
62.	Which LangChain class is used? 
63.	How do we load the embedding model? 
64.	How are document embeddings generated? 
65.	How are query embeddings generated? 
66.	How are embeddings stored? 
67.	Can embeddings be reused? 
68.	Can embeddings be updated? 
69.	Can embeddings be deleted? 
70.	How do we verify successful embedding generation? 
________________________________________
Section 8 – Advantages
71.	What are the advantages of embeddings? 
72.	Why are embeddings better than keyword search? 
73.	How do embeddings improve semantic understanding? 
74.	How do embeddings improve retrieval quality? 
75.	How do embeddings reduce irrelevant retrieval? 
76.	Why are embeddings important in modern AI systems? 
77.	How do embeddings improve question answering? 
78.	Why are embeddings used in almost every RAG system? 
79.	How do embeddings improve scalability? 
80.	How do embeddings improve user experience? 
________________________________________
Section 9 – Limitations
81.	What are the limitations of embeddings? 
82.	Can embeddings make mistakes? 
83.	Can similar meanings produce different embeddings? 
84.	Can embeddings be affected by poor chunking? 
85.	Can embeddings be affected by noisy text? 
86.	Can embeddings consume large storage? 
87.	Can embeddings increase computation time? 
88.	Why do embedding models need updates? 
89.	Can embeddings introduce bias? 
90.	How can embedding quality be improved? 
________________________________________
Section 10 – Comparisons
91.	Keyword Search vs Embedding Search 
92.	TF-IDF vs Embeddings 
93.	BM25 vs Embeddings 
94.	Sparse Retrieval vs Dense Retrieval 
95.	One-Hot Encoding vs Embeddings 
96.	Word Embeddings vs Sentence Embeddings 
97.	Static Embeddings vs Contextual Embeddings 
98.	BGE vs OpenAI Embeddings 
99.	BGE vs E5 Embeddings 
100.	Which embedding model is most suitable for ResearchMind? 
________________________________________
Section 11 – Project Perspective
101.	Why are embeddings required in ResearchMind? 
102.	Where are embeddings used in the project? 
103.	Which module depends on embeddings? 
104.	How do embeddings support Dense Retrieval? 
105.	How do embeddings support Hybrid Retrieval? 
106.	How do embeddings support the reranker? 
107.	Do embeddings directly interact with the LLM? 
108.	How do embeddings improve answer generation? 
109.	What happens if embeddings are generated incorrectly? 
110.	Can the project work without embeddings? 
________________________________________
Section 12 – Coding & Testing
111.	Which package should be installed to generate embeddings? 
112.	How do you initialize the embedding model? 
113.	What input format does the embedding model expect? 
114.	What output format does it produce? 
115.	How can you print an embedding vector? 
116.	How can you verify that embeddings were generated correctly? 
117.	How do you regenerate embeddings after adding new documents? 
118.	What errors can occur during embedding generation? 
119.	How do you debug embedding-related issues? 
120.	What test cases should be prepared for the embedding module? 
________________________________________
Section 13 – Management Questions
121.	Why do we need embeddings? 
122.	Why not directly compare text? 
123.	Why did you choose the BGE embedding model? 
124.	Why not OpenAI embeddings? 
125.	Why not Sentence-BERT? 
126.	Can embeddings understand meaning? 
127.	Can embeddings retrieve exact keywords? 
128.	What happens if embeddings are poor? 
129.	How do embeddings affect the overall performance of ResearchMind? 
130.	If you redesign the embedding module, what improvements would you make?

MODULE 5 – VECTOR DATABASE
Chapter 8 – ChromaDB (Vector Database)
________________________________________
Section 1 – Introduction
Understanding
1.	What is a vector database? 
2.	Why is a vector database required in ResearchMind? 
3.	What is stored in a vector database? 
4.	At which stage of the ResearchMind pipeline is the vector database used? 
5.	What is the input to the vector database? 
6.	What is the output from the vector database? 
7.	Can ResearchMind work without a vector database? 
8.	What happens before storing data in the vector database? 
9.	What happens after retrieving data from the vector database? 
10.	Why is a vector database different from a traditional database? 
________________________________________
Section 2 – ChromaDB
11.	What is ChromaDB? 
12.	Why are we using ChromaDB? 
13.	Is ChromaDB open source? 
14.	Which programming language supports ChromaDB? 
15.	Which framework easily integrates with ChromaDB? 
16.	Is ChromaDB suitable for beginners? 
17.	Can ChromaDB run locally? 
18.	Can ChromaDB be deployed on a server? 
19.	Why is ChromaDB suitable for ResearchMind? 
20.	What are the main features of ChromaDB? 
________________________________________
Section 3 – Data Storage
21.	What information is stored in ChromaDB? 
22.	Does ChromaDB store complete PDFs? 
23.	Does ChromaDB store text chunks? 
24.	Does ChromaDB store embeddings? 
25.	Does ChromaDB store metadata? 
26.	Why are embeddings stored instead of raw text? 
27.	How are embeddings linked to their original chunks? 
28.	How are metadata linked to embeddings? 
29.	Can ChromaDB store multiple research papers? 
30.	Can duplicate embeddings exist? 
________________________________________
Section 4 – Collections
31.	What is a collection in ChromaDB? 
32.	Why are collections required? 
33.	How are collections created? 
34.	Can multiple collections exist? 
35.	Can collections be deleted? 
36.	Can collections be updated? 
37.	Can one collection contain multiple research papers? 
38.	Can different domains have different collections? 
39.	How are collections searched? 
40.	Why are collections useful? 
________________________________________
Section 5 – Similarity Search
41.	What is similarity search? 
42.	Why is similarity search required? 
43.	How does ChromaDB perform similarity search? 
44.	Does ChromaDB compare text or embeddings? 
45.	How does ChromaDB identify similar vectors? 
46.	Which similarity measure is commonly used? 
47.	What is Top-K retrieval? 
48.	How many chunks should be retrieved? 
49.	Why don't we retrieve every chunk? 
50.	How are retrieved chunks ranked before reranking? 
________________________________________
Section 6 – CRUD Operations
51.	How are embeddings inserted into ChromaDB? 
52.	Can new research papers be added later? 
53.	Can existing embeddings be updated? 
54.	Can embeddings be deleted? 
55.	What happens when a paper is removed? 
56.	Can ChromaDB automatically update itself? 
57.	How do we rebuild the knowledge base? 
58.	What happens if duplicate embeddings are inserted? 
59.	How do we verify successful insertion? 
60.	How do we verify successful retrieval? 
________________________________________
Section 7 – Practical Implementation
61.	Which Python library is used? 
62.	Which LangChain class integrates ChromaDB? 
63.	How do we create a ChromaDB instance? 
64.	How do we create a collection? 
65.	How do we insert embeddings? 
66.	How do we retrieve similar chunks? 
67.	How do we delete a collection? 
68.	How do we reload an existing database? 
69.	How do we save the database permanently? 
70.	How do we check whether the database contains data? 
________________________________________
Section 8 – Advantages
71.	What are the advantages of ChromaDB? 
72.	Why is ChromaDB suitable for RAG? 
73.	Why is ChromaDB faster than searching PDFs directly? 
74.	Why is ChromaDB scalable? 
75.	How does ChromaDB improve retrieval speed? 
76.	Why is ChromaDB easy to integrate with LangChain? 
77.	How does ChromaDB support semantic search? 
78.	Why is ChromaDB suitable for student projects? 
79.	Why is ChromaDB popular in RAG applications? 
80.	How does ChromaDB improve the overall performance of ResearchMind? 
________________________________________
Section 9 – Limitations
81.	What are the limitations of ChromaDB? 
82.	Can ChromaDB store billions of vectors? 
83.	What happens if storage becomes full? 
84.	Can ChromaDB become slow? 
85.	Can ChromaDB lose data? 
86.	How can database corruption be handled? 
87.	What happens if embeddings are incorrect? 
88.	Can poor metadata affect retrieval? 
89.	How can ChromaDB performance be improved? 
90.	When should another vector database be considered? 
________________________________________
Section 10 – Comparisons
91.	ChromaDB vs FAISS 
92.	ChromaDB vs Pinecone 
93.	ChromaDB vs Qdrant 
94.	ChromaDB vs Weaviate 
95.	ChromaDB vs Milvus 
96.	ChromaDB vs MySQL 
97.	ChromaDB vs MongoDB 
98.	Why not use a relational database? 
99.	Which vector database is best for undergraduate projects? 
100.	Why was ChromaDB selected for ResearchMind? 
________________________________________
Section 11 – Project Perspective
101.	Where is ChromaDB used in ResearchMind? 
102.	Which module sends data to ChromaDB? 
103.	Which module retrieves data from ChromaDB? 
104.	How does ChromaDB support Hybrid Retrieval? 
105.	How does ChromaDB support Section-Aware Retrieval? 
106.	How does ChromaDB support Dynamic Research Paper Ingestion? 
107.	What happens if ChromaDB is removed? 
108.	Can another vector database replace ChromaDB? 
109.	How does ChromaDB affect answer quality? 
110.	Which future improvements can be made to this module? 
________________________________________
Section 12 – Coding & Testing
111.	How do you install ChromaDB? 
112.	How do you create a persistent database? 
113.	How do you insert one document? 
114.	How do you insert multiple documents? 
115.	How do you retrieve the Top-K similar chunks? 
116.	How do you verify successful retrieval? 
117.	How do you update an existing document? 
118.	How do you delete a document? 
119.	How do you test the vector database? 
120.	What debugging steps should be followed if retrieval fails? 
________________________________________
Section 13 – Management Questions
121.	Why did you choose ChromaDB? 
122.	Why not FAISS? 
123.	Why not Pinecone? 
124.	Why not MongoDB? 
125.	Why not MySQL? 
126.	What exactly is stored inside ChromaDB? 
127.	How many embeddings can ChromaDB store? 
128.	How will ChromaDB support newly added research papers? 
129.	Can ChromaDB retrieve documents without embeddings? 
130.	If ResearchMind is deployed for a university with one million research papers, will ChromaDB still be the best choice? Why or why not?

MODULE 6 – INFORMATION RETRIEVAL
Chapter 9 – BM25 (Sparse Retrieval)
________________________________________
Section 1 – Introduction to Information Retrieval
Understanding
1.	What is Information Retrieval? 
2.	Why is Information Retrieval required? 
3.	Where is Information Retrieval used? 
4.	What is the objective of an Information Retrieval system? 
5.	How is Information Retrieval different from Database Retrieval? 
6.	What is the role of Information Retrieval in ResearchMind? 
7.	At which stage of the ResearchMind pipeline is Information Retrieval performed? 
8.	What is the input to the retrieval module? 
9.	What is the output of the retrieval module? 
10.	What happens after retrieval? 
________________________________________
Section 2 – Introduction to BM25
11.	What is BM25? 
12.	What does BM25 stand for? 
13.	Is BM25 an algorithm or a machine learning model? 
14.	What type of retrieval technique is BM25? 
15.	Why was BM25 developed? 
16.	What problem does BM25 solve? 
17.	Where is BM25 commonly used? 
18.	Why is BM25 still widely used today? 
19.	Does BM25 require training? 
20.	Why is BM25 called a sparse retrieval technique? 
________________________________________
Section 3 – Working of BM25
21.	How does BM25 work? 
22.	What is the input to BM25? 
23.	What is the output of BM25? 
24.	How does BM25 search documents? 
25.	What is keyword matching? 
26.	How does BM25 calculate document relevance? 
27.	What happens when a keyword appears multiple times? 
28.	How does BM25 rank documents? 
29.	How are the highest-ranking chunks selected? 
30.	What happens after BM25 retrieves the chunks? 
________________________________________
Section 4 – BM25 Components
31.	What is Term Frequency (TF)? 
32.	Why is Term Frequency important? 
33.	What is Inverse Document Frequency (IDF)? 
34.	Why is IDF important? 
35.	What is document length normalization? 
36.	Why does BM25 consider document length? 
37.	Why are common words given less importance? 
38.	How are rare words handled? 
39.	Which parameters influence BM25 scoring? 
40.	Why is BM25 considered a ranking algorithm? 
________________________________________
Section 5 – Practical Usage
41.	Which data does BM25 search? 
42.	Does BM25 search complete research papers? 
43.	Does BM25 search chunks? 
44.	Does BM25 search embeddings? 
45.	Does BM25 require a vector database? 
46.	Does BM25 require embeddings? 
47.	Can BM25 work independently? 
48.	Can BM25 retrieve documents without an LLM? 
49.	How many chunks should BM25 retrieve? 
50.	What happens after BM25 retrieves the chunks? 
________________________________________
Section 6 – Advantages
51.	What are the advantages of BM25? 
52.	Why is BM25 computationally efficient? 
53.	Why is BM25 suitable for exact keyword matching? 
54.	Why is BM25 faster than semantic search? 
55.	Why is BM25 easy to implement? 
56.	Why is BM25 widely used in search engines? 
57.	Why is BM25 useful for research papers? 
58.	How does BM25 improve retrieval speed? 
59.	How does BM25 reduce computational cost? 
60.	Why is BM25 still relevant in modern RAG systems? 
________________________________________
Section 7 – Limitations
61.	What are the limitations of BM25? 
62.	Can BM25 understand sentence meaning? 
63.	Can BM25 understand context? 
64.	Can BM25 identify synonyms? 
65.	What happens if the user uses different terminology? 
66.	Why can BM25 miss relevant documents? 
67.	Why is BM25 not sufficient alone in ResearchMind? 
68.	Can BM25 retrieve semantically similar chunks? 
69.	Can BM25 increase false negatives? 
70.	How can these limitations be addressed? 
________________________________________
Section 8 – Comparisons
71.	BM25 vs TF-IDF 
72.	BM25 vs Keyword Search 
73.	BM25 vs Dense Retrieval 
74.	BM25 vs Semantic Search 
75.	BM25 vs Hybrid Retrieval 
76.	Which technique is faster? 
77.	Which technique provides better semantic understanding? 
78.	Which technique is more suitable for exact keyword matching? 
79.	Why is BM25 combined with Dense Retrieval? 
80.	Why isn't BM25 replaced completely by Dense Retrieval? 
________________________________________
Section 9 – BM25 in ResearchMind
81.	Where is BM25 used in ResearchMind? 
82.	At which stage does BM25 operate? 
83.	Which module provides the chunks to BM25? 
84.	Which module receives BM25 results? 
85.	Does BM25 use section metadata? 
86.	How does BM25 support Hybrid Retrieval? 
87.	Why is BM25 important in our project? 
88.	What happens if BM25 is removed? 
89.	Which types of queries are handled well by BM25? 
90.	Which types of queries are difficult for BM25? 
________________________________________
Section 10 – Practical Implementation
91.	Which Python library provides BM25? 
92.	How is BM25 implemented in Python? 
93.	How are chunks indexed? 
94.	How is a query processed? 
95.	How are BM25 scores generated? 
96.	How are the Top-K chunks selected? 
97.	How can BM25 results be displayed? 
98.	How can BM25 performance be tested? 
99.	How can BM25 be integrated with LangChain? 
100.	What debugging steps should be followed if BM25 retrieves incorrect results? 
________________________________________
Section 11 – Performance & Evaluation
101.	How do we evaluate BM25? 
102.	How can retrieval accuracy be measured? 
103.	How do we know BM25 is retrieving relevant chunks? 
104.	How does chunk size affect BM25? 
105.	How does poor preprocessing affect BM25? 
106.	How does duplicate data affect BM25? 
107.	Can BM25 retrieve irrelevant chunks? 
108.	How can BM25 retrieval quality be improved? 
109.	Which evaluation metrics can be used for BM25? 
110.	How can BM25 results be compared with Dense Retrieval? 
________________________________________
Section 12 – Management Questions
111.	Why did you include BM25 in ResearchMind? 
112.	Why not use only Dense Retrieval? 
113.	Why not use only keyword search? 
114.	Does BM25 require machine learning? 
115.	Does BM25 require training? 
116.	Can BM25 retrieve newly added research papers? 
117.	How does BM25 handle spelling mistakes? 
118.	What happens if the user query contains no matching keywords? 
119.	How does BM25 contribute to Hybrid Retrieval? 
120.	If BM25 is removed from ResearchMind, what impact will it have? 
________________________________________
Section 13 – Critical Thinking
121.	Can BM25 be improved? 
122.	Can BM25 use metadata during retrieval? 
123.	Can BM25 be combined with Explainable AI? 
124.	Can BM25 learn from user feedback? 
125.	What future improvements can be added to BM25? 
126.	Would BM25 perform well for multilingual research papers? 
127.	Would BM25 perform well for image-based documents? 
128.	Can BM25 be used outside RAG applications? 
129.	If you redesign BM25 for ResearchMind, what changes would you make? 
130.	In which situations should BM25 not be used?

MODULE 6 – INFORMATION RETRIEVAL
Chapter 10 – Dense Retrieval (Semantic Retrieval)
________________________________________
Section 1 – Introduction
Understanding
1.	What is Dense Retrieval? 
2.	Why is Dense Retrieval required? 
3.	What problem does Dense Retrieval solve? 
4.	Where is Dense Retrieval used? 
5.	At which stage of the ResearchMind pipeline is Dense Retrieval performed? 
6.	What is the input to Dense Retrieval? 
7.	What is the output of Dense Retrieval? 
8.	Why is Dense Retrieval also called Semantic Retrieval? 
9.	Can Dense Retrieval work without embeddings? 
10.	What happens after Dense Retrieval retrieves the relevant chunks? 
________________________________________
Section 2 – Need for Dense Retrieval
11.	Why is BM25 alone not sufficient? 
12.	What are the limitations of BM25 that Dense Retrieval addresses? 
13.	Why is semantic understanding important? 
14.	How does Dense Retrieval understand the meaning of a query? 
15.	Why can Dense Retrieval retrieve documents even when exact keywords are not present? 
16.	Why is semantic search better than keyword search in some cases? 
17.	Which types of queries are better handled by Dense Retrieval? 
18.	Can Dense Retrieval retrieve contextually similar information? 
19.	Why is Dense Retrieval widely used in modern RAG systems? 
20.	Why is Dense Retrieval important in ResearchMind? 
________________________________________
Section 3 – Working of Dense Retrieval
21.	How does Dense Retrieval work? 
22.	What is the first step in Dense Retrieval? 
23.	How is the user query converted into an embedding? 
24.	How are document chunks converted into embeddings? 
25.	How are query embeddings compared with document embeddings? 
26.	What happens after similarity calculation? 
27.	How are the Top-K chunks selected? 
28.	Which module receives the retrieved chunks? 
29.	Does Dense Retrieval generate answers? 
30.	How does Dense Retrieval differ from BM25 internally? 
________________________________________
Section 4 – Embedding Model
31.	Which embedding model is used in ResearchMind? 
32.	Why did we choose the BGE embedding model? 
33.	Can another embedding model be used? 
34.	What is the role of the embedding model? 
35.	Why should the same embedding model be used for both queries and documents? 
36.	Can different embedding models produce different retrieval results? 
37.	How does embedding quality affect Dense Retrieval? 
38.	Can poor embeddings reduce retrieval accuracy? 
39.	What happens if embeddings are missing? 
40.	Can Dense Retrieval work without generating embeddings? 
________________________________________
Section 5 – Similarity Search
41.	How does Dense Retrieval identify similar chunks? 
42.	What is cosine similarity? 
43.	Why is cosine similarity commonly used? 
44.	What is dot product similarity? 
45.	What is Euclidean distance? 
46.	Which similarity measure is used in our project? 
47.	How are similarity scores generated? 
48.	What does a higher similarity score indicate? 
49.	Why are only the Top-K chunks selected? 
50.	Can similarity search retrieve irrelevant chunks? 
________________________________________
Section 6 – Bi-Encoder Retriever
51.	What is a Bi-Encoder Retriever? 
52.	Why is it called a Bi-Encoder? 
53.	How does the Bi-Encoder work? 
54.	Why is the Bi-Encoder used in Dense Retrieval? 
55.	How are document embeddings generated by the Bi-Encoder? 
56.	How are query embeddings generated? 
57.	Can document embeddings be generated in advance? 
58.	Why is query embedding generated at runtime? 
59.	Why is the Bi-Encoder considered efficient? 
60.	What are the limitations of a Bi-Encoder? 
________________________________________
Section 7 – Practical Implementation
61.	Which Python libraries are used for Dense Retrieval? 
62.	Which LangChain components are used? 
63.	How do we load the embedding model? 
64.	How do we generate document embeddings? 
65.	How do we generate query embeddings? 
66.	How do we retrieve the Top-K similar chunks? 
67.	How is Dense Retrieval connected to ChromaDB? 
68.	How do we verify successful retrieval? 
69.	How can Dense Retrieval be tested? 
70.	What debugging steps should be followed if Dense Retrieval retrieves incorrect chunks? 
________________________________________
Section 8 – Advantages
71.	What are the advantages of Dense Retrieval? 
72.	Why is Dense Retrieval better at understanding meaning? 
73.	How does Dense Retrieval improve retrieval quality? 
74.	How does Dense Retrieval improve answer quality? 
75.	Why is Dense Retrieval suitable for research papers? 
76.	How does Dense Retrieval support semantic search? 
77.	Why is Dense Retrieval widely used in RAG systems? 
78.	How does Dense Retrieval improve user experience? 
79.	Why is Dense Retrieval scalable? 
80.	Why is Dense Retrieval suitable for ResearchMind? 
________________________________________
Section 9 – Limitations
81.	What are the limitations of Dense Retrieval? 
82.	Does Dense Retrieval require embeddings? 
83.	Does Dense Retrieval require a vector database? 
84.	Can Dense Retrieval retrieve incorrect chunks? 
85.	Can Dense Retrieval miss exact keyword matches? 
86.	How does poor chunking affect Dense Retrieval? 
87.	How does poor preprocessing affect Dense Retrieval? 
88.	Can Dense Retrieval consume more memory? 
89.	Can Dense Retrieval be slower than BM25? 
90.	How can these limitations be addressed? 
________________________________________
Section 10 – Comparisons
91.	Dense Retrieval vs BM25 
92.	Dense Retrieval vs Keyword Search 
93.	Dense Retrieval vs TF-IDF 
94.	Dense Retrieval vs Semantic Search 
95.	Dense Retrieval vs Hybrid Retrieval 
96.	Bi-Encoder vs Cross-Encoder 
97.	Sparse Retrieval vs Dense Retrieval 
98.	Which retrieval technique is more accurate? 
99.	Which retrieval technique is computationally faster? 
100.	Why do we combine Dense Retrieval with BM25? 
________________________________________
Section 11 – Dense Retrieval in ResearchMind
101.	Where is Dense Retrieval used in ResearchMind? 
102.	Which module provides the query embedding? 
103.	Which module provides the document embeddings? 
104.	Which module receives the retrieved chunks? 
105.	How does Dense Retrieval support Hybrid Retrieval? 
106.	How does Dense Retrieval support Section-Aware Retrieval? 
107.	How does Dense Retrieval support Evidence Highlighting? 
108.	What happens if Dense Retrieval is removed? 
109.	Which queries are better handled by Dense Retrieval? 
110.	How does Dense Retrieval contribute to the overall system? 
________________________________________
Section 12 – Performance & Evaluation
111.	How do we evaluate Dense Retrieval? 
112.	Which evaluation metrics can be used? 
113.	How do we verify retrieval accuracy? 
114.	How can we compare Dense Retrieval with BM25? 
115.	How do embeddings influence retrieval quality? 
116.	How does chunk size affect Dense Retrieval? 
117.	How does metadata affect retrieval? 
118.	How many chunks should Dense Retrieval retrieve? 
119.	How can retrieval performance be improved? 
120.	How do we verify that Dense Retrieval is working correctly? 
________________________________________
Section 13 – Management Questions
121.	Why did you include Dense Retrieval? 
122.	Why not use only BM25? 
123.	Why is Dense Retrieval called semantic retrieval? 
124.	How does Dense Retrieval understand meaning? 
125.	Why did you choose the BGE embedding model? 
126.	Can Dense Retrieval work without ChromaDB? 
127.	What happens if embeddings are generated incorrectly? 
128.	Which retrieval technique is more important—BM25 or Dense Retrieval? 
129.	If you remove Dense Retrieval from ResearchMind, what will happen? 
130.	If you redesign this module, what improvements would you make? 
________________________________________
Section 14 – Critical Thinking
131.	Can Dense Retrieval learn from user feedback? 
132.	Can Dense Retrieval work for multilingual documents? 
133.	Can Dense Retrieval retrieve information from images? 
134.	How would you improve Dense Retrieval for research papers? 
135.	What future research directions exist in Dense Retrieval? 
136.	Can Dense Retrieval be used outside RAG applications? 
137.	What challenges arise when the dataset grows to millions of documents? 
138.	Can Dense Retrieval be combined with knowledge graphs? 
139.	How will Dense Retrieval evolve in future AI systems? 
140.	In which situations should Dense Retrieval not be used?

MODULE 6 – INFORMATION RETRIEVAL
Chapter 11 – Hybrid Retrieval
________________________________________
Section 1 – Introduction
Understanding
1.	What is Hybrid Retrieval? 
2.	Why is Hybrid Retrieval required? 
3.	What problem does Hybrid Retrieval solve? 
4.	Where is Hybrid Retrieval used? 
5.	At which stage of the ResearchMind pipeline is Hybrid Retrieval performed? 
6.	What is the input to Hybrid Retrieval? 
7.	What is the output of Hybrid Retrieval? 
8.	Why is Hybrid Retrieval considered an enhancement over traditional retrieval? 
9.	Can ResearchMind work without Hybrid Retrieval? 
10.	What happens after Hybrid Retrieval? 
________________________________________
Section 2 – Need for Hybrid Retrieval
11.	Why is BM25 alone not sufficient? 
12.	Why is Dense Retrieval alone not sufficient? 
13.	What are the limitations of BM25? 
14.	What are the limitations of Dense Retrieval? 
15.	Why do we combine keyword search and semantic search? 
16.	How does Hybrid Retrieval improve retrieval quality? 
17.	How does Hybrid Retrieval reduce missed relevant documents? 
18.	How does Hybrid Retrieval improve answer quality? 
19.	Why is Hybrid Retrieval suitable for research papers? 
20.	Why is Hybrid Retrieval one of the main novelties of ResearchMind? 
________________________________________
Section 3 – Internal Working
21.	How does Hybrid Retrieval work? 
22.	Which retrieval techniques are combined? 
23.	Does BM25 execute first? 
24.	Does Dense Retrieval execute first? 
25.	Can both retrieval techniques run simultaneously? 
26.	How are BM25 results collected? 
27.	How are Dense Retrieval results collected? 
28.	How are the retrieved results merged? 
29.	How is the final candidate list prepared? 
30.	What happens after Hybrid Retrieval? 
________________________________________
Section 4 – Merging Results
31.	How are BM25 results merged with Dense Retrieval results? 
32.	How are duplicate chunks identified? 
33.	How are duplicate chunks removed? 
34.	What happens if BM25 and Dense Retrieval return the same chunk? 
35.	What happens if they return completely different chunks? 
36.	How is the final candidate list prepared? 
37.	Does the order of retrieved chunks matter? 
38.	Why is merging important? 
39.	Which module receives the merged results? 
40.	Why is reranking required after merging? 
________________________________________
Section 5 – Practical Implementation
41.	Which LangChain component supports Hybrid Retrieval? 
42.	What is EnsembleRetriever? 
43.	Why are we using EnsembleRetriever? 
44.	How does EnsembleRetriever work? 
45.	Which retrievers are connected to it? 
46.	How are weights assigned? 
47.	Can different weights be used? 
48.	Why are retrieval weights important? 
49.	Can Hybrid Retrieval be implemented without LangChain? 
50.	How do we verify that Hybrid Retrieval is working correctly? 
________________________________________
Section 6 – Retrieval Weights
51.	What are retrieval weights? 
52.	Why are weights assigned? 
53.	How do weights affect retrieval? 
54.	Can BM25 and Dense Retrieval have equal weights? 
55.	Can BM25 be given a higher weight? 
56.	Can Dense Retrieval be given a higher weight? 
57.	How do we decide the weights? 
58.	Can weights be changed later? 
59.	How do weights affect retrieval quality? 
60.	What happens if incorrect weights are selected? 
________________________________________
Section 7 – Top-K Selection
61.	What is Top-K retrieval? 
62.	Why is Top-K retrieval required? 
63.	How many chunks should BM25 retrieve? 
64.	How many chunks should Dense Retrieval retrieve? 
65.	How many chunks are finally merged? 
66.	How many chunks are passed to the reranker? 
67.	How do we decide the value of K? 
68.	What happens if K is too small? 
69.	What happens if K is too large? 
70.	How does Top-K affect performance? 
________________________________________
Section 8 – Advantages
71.	What are the advantages of Hybrid Retrieval? 
72.	Why is Hybrid Retrieval more reliable than BM25? 
73.	Why is Hybrid Retrieval more reliable than Dense Retrieval? 
74.	How does Hybrid Retrieval improve retrieval accuracy? 
75.	How does Hybrid Retrieval improve semantic understanding? 
76.	How does Hybrid Retrieval reduce missing relevant information? 
77.	How does Hybrid Retrieval improve answer generation? 
78.	Why is Hybrid Retrieval suitable for scientific literature? 
79.	How does Hybrid Retrieval improve user satisfaction? 
80.	Why is Hybrid Retrieval recommended for modern RAG systems? 
________________________________________
Section 9 – Limitations
81.	What are the limitations of Hybrid Retrieval? 
82.	Does Hybrid Retrieval increase computation time? 
83.	Does Hybrid Retrieval require more memory? 
84.	Can Hybrid Retrieval retrieve duplicate chunks? 
85.	Can poor BM25 results affect Hybrid Retrieval? 
86.	Can poor embeddings affect Hybrid Retrieval? 
87.	Does Hybrid Retrieval require tuning? 
88.	Can incorrect weights reduce performance? 
89.	Can Hybrid Retrieval still retrieve irrelevant chunks? 
90.	How can these limitations be reduced? 
________________________________________
Section 10 – Comparisons
91.	BM25 vs Hybrid Retrieval 
92.	Dense Retrieval vs Hybrid Retrieval 
93.	Hybrid Retrieval vs Semantic Search 
94.	Hybrid Retrieval vs Keyword Search 
95.	Hybrid Retrieval vs Traditional RAG 
96.	Hybrid Retrieval vs OpenScholar Retrieval 
97.	Which retrieval technique provides better recall? 
98.	Which retrieval technique provides better precision? 
99.	Which retrieval technique is more suitable for ResearchMind? 
100.	Why was Hybrid Retrieval selected instead of using a single retriever? 
________________________________________
Section 11 – Hybrid Retrieval in ResearchMind
101.	Where is Hybrid Retrieval used in ResearchMind? 
102.	Which modules provide input to Hybrid Retrieval? 
103.	Which module receives the retrieved chunks? 
104.	How does Hybrid Retrieval support Section-Aware Retrieval? 
105.	How does Hybrid Retrieval improve Evidence Highlighting? 
106.	How does Hybrid Retrieval improve Groundedness Assessment? 
107.	How does Hybrid Retrieval improve Trust Score generation? 
108.	What happens if Hybrid Retrieval is removed? 
109.	Which future modules depend on Hybrid Retrieval? 
110.	Why is Hybrid Retrieval considered the major improvement over the base paper? 
________________________________________
Section 12 – Performance Evaluation
111.	How do we evaluate Hybrid Retrieval? 
112.	Which evaluation metrics are suitable? 
113.	How do we compare Hybrid Retrieval with BM25? 
114.	How do we compare Hybrid Retrieval with Dense Retrieval? 
115.	How do we verify retrieval quality? 
116.	How do we measure retrieval accuracy? 
117.	How do we measure context relevance? 
118.	How do we verify that Hybrid Retrieval improves performance? 
119.	What experiments should be performed? 
120.	How should experimental results be presented? 
________________________________________
Section 13 – Practical & Coding Questions
121.	Which Python libraries are required for Hybrid Retrieval? 
122.	How do you create a BM25 retriever? 
123.	How do you create a Dense Retriever? 
124.	How do you combine both retrievers? 
125.	How do you configure EnsembleRetriever? 
126.	How do you specify retrieval weights? 
127.	How do you specify Top-K? 
128.	How do you test Hybrid Retrieval? 
129.	How do you debug incorrect retrieval results? 
130.	Which module should be tested before Hybrid Retrieval? 
________________________________________
Section 14 – Management Questions
131.	Why did you introduce Hybrid Retrieval? 
132.	Why not use only BM25? 
133.	Why not use only Dense Retrieval? 
134.	Why is Hybrid Retrieval better than OpenScholar's retrieval approach? 
135.	How does Hybrid Retrieval improve the quality of retrieved chunks? 
136.	How do you prove Hybrid Retrieval is better? 
137.	What happens if BM25 fails? 
138.	What happens if Dense Retrieval fails? 
139.	Can Hybrid Retrieval work if one retriever is unavailable? 
140.	If you remove Hybrid Retrieval from ResearchMind, what effect will it have on the overall system? 
________________________________________
Section 15 – Critical Thinking
141.	Can Hybrid Retrieval be improved further? 
142.	Can retrieval weights be adjusted automatically? 
143.	Can Hybrid Retrieval learn from user feedback? 
144.	Can metadata influence Hybrid Retrieval? 
145.	Can Section-Aware Retrieval be integrated directly into Hybrid Retrieval? 
146.	How will Hybrid Retrieval perform with one million research papers? 
147.	What future research directions exist for Hybrid Retrieval? 
148.	Can Hybrid Retrieval be applied outside research paper analysis? 
149.	If you redesign the Hybrid Retrieval module, what improvements would you make? 
150.	Is Hybrid Retrieval the best possible retrieval approach, or can it be further improved?
MODULE 7 – RERANKING
Chapter 12 – Cross-Encoder Reranker
________________________________________
Section 1 – Why Reranking?
Understanding
1.	What is reranking? 
2.	Why is reranking required in ResearchMind? 
3.	Why isn't Hybrid Retrieval alone sufficient? 
4.	What problem does reranking solve? 
5.	At which stage of the ResearchMind pipeline is reranking performed? 
6.	What is the input to the reranker? 
7.	What is the output of the reranker? 
8.	Why is reranking performed before the LLM? 
9.	Can the project work without reranking? 
10.	What happens after reranking? 
________________________________________
Section 2 – Need for Reranking
11.	Why can BM25 retrieve irrelevant chunks? 
12.	Why can Dense Retrieval retrieve irrelevant chunks? 
13.	Why can Hybrid Retrieval still retrieve unnecessary chunks? 
14.	Why shouldn't all retrieved chunks be sent to the LLM? 
15.	What happens if irrelevant chunks are sent to the LLM? 
16.	How does reranking improve answer quality? 
17.	How does reranking reduce hallucination? 
18.	How does reranking improve context quality? 
19.	Why is reranking important for scientific literature? 
20.	Why is reranking considered a quality improvement step? 
________________________________________
Section 3 – Cross-Encoder
21.	What is a Cross-Encoder? 
22.	Why is it called a Cross-Encoder? 
23.	What is the purpose of a Cross-Encoder? 
24.	How does a Cross-Encoder work? 
25.	What is the input to the Cross-Encoder? 
26.	What is the output of the Cross-Encoder? 
27.	Why does it process the query and document together? 
28.	How does it calculate relevance? 
29.	Does it generate answers? 
30.	What happens after scoring? 
________________________________________
Section 4 – Bi-Encoder vs Cross-Encoder
31.	What is a Bi-Encoder? 
32.	What is a Cross-Encoder? 
33.	How does a Bi-Encoder process text? 
34.	How does a Cross-Encoder process text? 
35.	Why is the Bi-Encoder faster? 
36.	Why is the Cross-Encoder more accurate? 
37.	Why isn't the Cross-Encoder used for the initial retrieval? 
38.	Why isn't the Bi-Encoder used for reranking? 
39.	Why are both models required? 
40.	How do they complement each other? 
________________________________________
Section 5 – Internal Working
41.	How does the reranking process start? 
42.	Which chunks are given to the Cross-Encoder? 
43.	How does the Cross-Encoder score each chunk? 
44.	How are the chunks reordered? 
45.	What happens to low-scoring chunks? 
46.	How are the highest-scoring chunks selected? 
47.	How many chunks should be passed to the LLM? 
48.	Can the reranker change the retrieval order? 
49.	What happens if two chunks receive the same score? 
50.	Does reranking modify the chunk content? 
________________________________________
Section 6 – Practical Implementation
51.	Which reranker are we using in ResearchMind? 
52.	Why did we choose the BGE Cross-Encoder Reranker? 
53.	Which Python library provides the reranker? 
54.	Which LangChain components can be used? 
55.	How is the reranker loaded? 
56.	How are query-document pairs created? 
57.	How are relevance scores generated? 
58.	How are the results sorted? 
59.	How do we select the final Top-K chunks? 
60.	How do we verify that reranking is working correctly? 
________________________________________
Section 7 – Advantages
61.	What are the advantages of reranking? 
62.	Why does reranking improve retrieval quality? 
63.	Why does reranking improve answer accuracy? 
64.	How does reranking improve evidence quality? 
65.	Why does reranking reduce irrelevant context? 
66.	How does reranking improve user trust? 
67.	Why is reranking useful for research papers? 
68.	Why is reranking commonly used in modern RAG systems? 
69.	How does reranking improve Explainable AI? 
70.	Why is reranking important for ResearchMind? 
________________________________________
Section 8 – Limitations
71.	What are the limitations of reranking? 
72.	Why is reranking slower than retrieval? 
73.	Does reranking increase computation time? 
74.	Does reranking require additional memory? 
75.	Can reranking assign incorrect scores? 
76.	What happens if the retrieved chunks are already poor? 
77.	Can reranking recover missing chunks? 
78.	Can reranking increase latency? 
79.	How can reranking performance be improved? 
80.	When should reranking be avoided? 
________________________________________
Section 9 – Comparisons
81.	Retrieval vs Reranking 
82.	BM25 vs Cross-Encoder 
83.	Dense Retrieval vs Cross-Encoder 
84.	Bi-Encoder vs Cross-Encoder 
85.	Hybrid Retrieval vs Reranking 
86.	Can reranking replace retrieval? 
87.	Can retrieval replace reranking? 
88.	Which stage contributes more to answer quality? 
89.	Why do retrieval and reranking work together? 
90.	Why does OpenScholar use both retrieval and reranking? 
________________________________________
Section 10 – Reranking in ResearchMind
91.	Where is reranking used in ResearchMind? 
92.	Which module sends chunks to the reranker? 
93.	Which module receives the reranked chunks? 
94.	How does reranking improve Hybrid Retrieval? 
95.	How does reranking improve Section-Aware Retrieval? 
96.	How does reranking improve Evidence Highlighting? 
97.	How does reranking improve Groundedness Assessment? 
98.	How does reranking improve Trust Score generation? 
99.	What happens if reranking is removed from ResearchMind? 
100.	Why is reranking an essential part of our architecture? 
________________________________________
Section 11 – Performance Evaluation
101.	How do we evaluate the effectiveness of reranking? 
102.	How do we compare retrieval results before and after reranking? 
103.	Which evaluation metrics can be used? 
104.	How do we know reranking improves answer quality? 
105.	How does reranking affect Precision? 
106.	How does reranking affect Recall? 
107.	How does reranking affect Groundedness? 
108.	How does reranking affect Faithfulness? 
109.	How can reranking be experimentally validated? 
110.	How should reranking results be presented in the project report? 
________________________________________
Section 12 – Coding & Testing
111.	Which Python package is required for the Cross-Encoder? 
112.	How do you load the reranker model? 
113.	How do you create query-document pairs? 
114.	How do you generate relevance scores? 
115.	How do you sort the retrieved chunks? 
116.	How do you select the final Top-K chunks? 
117.	How do you test the reranker independently? 
118.	How do you debug incorrect reranking? 
119.	What unit tests should be written for the reranking module? 
120.	How do you verify that reranking improves retrieval? 
________________________________________
Section 13 – Management Questions
121.	Why is reranking required? 
122.	Why isn't Hybrid Retrieval alone sufficient? 
123.	Why did you choose a Cross-Encoder? 
124.	Why not use another Bi-Encoder for reranking? 
125.	Why is the Cross-Encoder slower? 
126.	Does reranking generate new information? 
127.	Can reranking retrieve missing chunks? 
128.	What happens if reranking is skipped? 
129.	How does reranking reduce hallucination? 
130.	If you remove the reranker, how will ResearchMind be affected? 
________________________________________
Section 14 – Critical Thinking
131.	Can reranking learn from user feedback? 
132.	Can reranking use metadata? 
133.	Can reranking consider section information? 
134.	Can reranking improve citation quality? 
135.	How can reranking be made faster? 
136.	Can multiple rerankers be combined? 
137.	What future improvements can be added to reranking? 
138.	How would reranking perform with one million research papers? 
139.	If you redesign the reranking module, what changes would you make? 
140.	Is reranking the final quality improvement step before the LLM? Why or why not? 
MODULE 8 – LARGE LANGUAGE MODELS
Chapter 13 – Large Language Models (LLMs)
________________________________________
Section 1 – Introduction to LLMs
Understanding
1.	What is an Artificial Intelligence (AI) model? 
2.	What is a language model? 
3.	What is a Large Language Model (LLM)? 
4.	Why is it called a Large Language Model? 
5.	Why are LLMs important in modern AI? 
6.	What problems can LLMs solve? 
7.	What are some popular Large Language Models? 
8.	Where are LLMs used? 
9.	Why are LLMs becoming popular? 
10.	What is the role of an LLM in ResearchMind? 
________________________________________
Section 2 – Need for an LLM
11.	Why do we need an LLM in ResearchMind? 
12.	Can ResearchMind work without an LLM? 
13.	Why can't retrieval alone answer user questions? 
14.	What happens after the retrieval module? 
15.	Why is answer generation required? 
16.	What is the input to the LLM? 
17.	What is the output of the LLM? 
18.	What information does the LLM receive? 
19.	Can the LLM search the database directly? 
20.	Why should the LLM use retrieved context? 
________________________________________
Section 3 – Working of an LLM
21.	How does an LLM work? 
22.	How does an LLM understand language? 
23.	How does an LLM generate text? 
24.	How does an LLM predict the next word? 
25.	What is tokenization? 
26.	What is a token? 
27.	Why are sentences converted into tokens? 
28.	What happens inside the LLM after tokenization? 
29.	How does the LLM generate complete sentences? 
30.	Does the LLM memorize answers? 
________________________________________
Section 4 – Transformer Architecture
31.	What is a Transformer? 
32.	Why are Transformers important? 
33.	What is the relationship between Transformers and LLMs? 
34.	What are the major components of a Transformer? 
35.	What is Self-Attention? 
36.	Why is Self-Attention important? 
37.	How does Self-Attention help understand context? 
38.	What is positional encoding? 
39.	Why do LLMs use Transformer architecture? 
40.	Can an LLM exist without a Transformer? 
________________________________________
Section 5 – Gemma 3
41.	What is Gemma 3? 
42.	Who developed Gemma 3? 
43.	Why did we choose Gemma 3? 
44.	Is Gemma 3 open source? 
45.	What are the advantages of Gemma 3? 
46.	Why is Gemma 3 suitable for student projects? 
47.	What versions of Gemma are available? 
48.	Which Gemma 3 model will we use? 
49.	How much hardware is required? 
50.	Can Gemma 3 run locally? 
________________________________________
Section 6 – Ollama
51.	What is Ollama? 
52.	Why are we using Ollama? 
53.	How does Ollama help run LLMs? 
54.	Which operating systems support Ollama? 
55.	Is Ollama free? 
56.	Can Ollama run offline? 
57.	How do we download Gemma 3 using Ollama? 
58.	How do we communicate with Gemma 3 through Ollama? 
59.	Can Ollama run multiple models? 
60.	Why is Ollama suitable for ResearchMind? 
________________________________________
Section 7 – Prompting
61.	What is a prompt? 
62.	Why is prompting important? 
63.	What is prompt engineering? 
64.	What information is included in the prompt? 
65.	How are retrieved chunks included in the prompt? 
66.	Why should the prompt be carefully designed? 
67.	How does prompt quality affect answer quality? 
68.	Can the same question produce different answers with different prompts? 
69.	What is a system prompt? 
70.	What is a user prompt? 
________________________________________
Section 8 – Context
71.	What is context? 
72.	Why is context important? 
73.	How is context generated? 
74.	Which module provides context? 
75.	What happens if incorrect context is given? 
76.	Can the LLM answer without context? 
77.	Why should only relevant chunks be passed? 
78.	What is the context window? 
79.	What happens if the context exceeds the limit? 
80.	How does context affect answer quality? 
________________________________________
Section 9 – Advantages
81.	What are the advantages of LLMs? 
82.	Why are LLMs suitable for question answering? 
83.	Why are LLMs suitable for research paper analysis? 
84.	How do LLMs improve user experience? 
85.	Why are LLMs better than rule-based systems? 
86.	How do LLMs understand natural language? 
87.	Why are LLMs flexible? 
88.	How do LLMs support ResearchMind? 
89.	Why are LLMs becoming the standard for AI assistants? 
90.	How do LLMs improve productivity? 
________________________________________
Section 10 – Limitations
91.	What are the limitations of LLMs? 
92.	What is hallucination? 
93.	Why do hallucinations occur? 
94.	Can LLMs generate incorrect information? 
95.	Why shouldn't we trust an LLM without retrieval? 
96.	Can LLMs produce biased answers? 
97.	Why do LLMs require large computational resources? 
98.	Can LLMs answer questions outside the provided context? 
99.	Why are LLMs combined with RAG? 
100.	How can hallucinations be reduced? 
________________________________________
Section 11 – Comparisons
101.	ChatGPT vs Gemma 3 
102.	Gemma 3 vs Llama 3 
103.	Gemma 3 vs Mistral 
104.	Gemma 3 vs DeepSeek 
105.	Open-source LLMs vs Closed-source LLMs 
106.	Cloud LLMs vs Local LLMs 
107.	Fine-tuning vs Prompting 
108.	LLM vs Traditional NLP Models 
109.	LLM vs Search Engine 
110.	Why was Gemma 3 selected for ResearchMind? 
________________________________________
Section 12 – LLM in ResearchMind
111.	Where is the LLM used in ResearchMind? 
112.	Which module sends information to the LLM? 
113.	Which module receives the LLM output? 
114.	Does the LLM perform retrieval? 
115.	Does the LLM perform reranking? 
116.	Does the LLM generate citations? 
117.	How does the LLM support Evidence Highlighting? 
118.	How does the LLM support Groundedness Assessment? 
119.	What happens if the LLM is removed? 
120.	Why is the LLM considered the answer generation engine of ResearchMind? 
________________________________________
Section 13 – Practical Implementation
121.	How do you install Ollama? 
122.	How do you download Gemma 3? 
123.	How do you verify that Gemma 3 is installed? 
124.	How do you run Gemma 3 locally? 
125.	How do you send a prompt to Gemma 3? 
126.	How do you receive the generated answer? 
127.	Which LangChain class communicates with Ollama? 
128.	How do you test the LLM independently? 
129.	How do you debug LLM-related errors? 
130.	How do you verify that the LLM is using the retrieved context? 
________________________________________
Section 14 – Management Questions
131.	Why did you choose Gemma 3? 
132.	Why not GPT-4? 
133.	Why not Llama 3? 
134.	Why are you running the model locally? 
135.	Why are you using Ollama? 
136.	Can Gemma 3 answer questions without retrieval? 
137.	What happens if incorrect context is provided? 
138.	Can the LLM generate answers outside the provided documents? 
139.	How does RAG reduce hallucination? 
140.	If you remove the LLM from ResearchMind, what functionality will be lost? 
________________________________________
Section 15 – Critical Thinking
141.	Can the LLM be replaced by another model? 
142.	Can multiple LLMs be used together? 
143.	Can the LLM learn from user feedback? 
144.	Can we fine-tune Gemma 3 for ResearchMind? 
145.	Is fine-tuning required for our project? 
146.	How would the project change if a cloud-based LLM were used? 
147.	How would the project change if a larger Gemma model were used? 
148.	What future improvements can be made to the LLM module? 
149.	If you redesign the LLM module, what changes would you make? 
150.	Why is the LLM considered the final intelligence layer of ResearchMind?
MODULE 9 – RETRIEVAL AUGMENTED GENERATION (RAG)
Chapter 14 – Answer Generation using RAG
________________________________________
Section 1 – Introduction
Understanding
1.	What is Retrieval-Augmented Generation (RAG)? 
2.	What does RAG stand for? 
3.	Why was RAG introduced? 
4.	What problem does RAG solve? 
5.	Why is RAG required in ResearchMind? 
6.	Where is RAG used? 
7.	What are the major components of a RAG system? 
8.	What is the role of retrieval in RAG? 
9.	What is the role of the LLM in RAG? 
10.	Why is RAG better than using an LLM alone? 
________________________________________
Section 2 – Need for RAG
11.	Why can't an LLM answer every question correctly? 
12.	What are the limitations of standalone LLMs? 
13.	Why do LLMs hallucinate? 
14.	How does RAG reduce hallucination? 
15.	Why is external knowledge required? 
16.	Why should the LLM use retrieved documents? 
17.	How does RAG improve answer quality? 
18.	Why is RAG suitable for research papers? 
19.	Why is RAG better than searching PDFs manually? 
20.	Why is RAG the foundation of ResearchMind? 
________________________________________
Section 3 – Complete Workflow
21.	Explain the complete workflow of RAG. 
22.	What is the first step in the RAG pipeline? 
23.	What is the last step in the RAG pipeline? 
24.	What happens immediately after the user enters a question? 
25.	Which module processes the user query? 
26.	Which modules perform retrieval? 
27.	Which module performs reranking? 
28.	Which module generates the final answer? 
29.	Which modules improve answer quality? 
30.	Draw the complete RAG workflow. 
________________________________________
Section 4 – Query Processing
31.	What is query processing? 
32.	What happens after the user enters a question? 
33.	Is the query converted into an embedding? 
34.	Why is the query embedding required? 
35.	Which embedding model is used? 
36.	Does BM25 also process the query? 
37.	Does Dense Retrieval also process the query? 
38.	Which retrieval techniques use the user query? 
39.	How is the query sent to the retrievers? 
40.	Can different queries produce different retrieval results? 
________________________________________
Section 5 – Retrieval
41.	What happens during retrieval? 
42.	Which retrievers are used in ResearchMind? 
43.	How does BM25 retrieve chunks? 
44.	How does Dense Retrieval retrieve chunks? 
45.	How are the retrieved chunks merged? 
46.	Why is Hybrid Retrieval required? 
47.	How many chunks are retrieved? 
48.	What happens after Hybrid Retrieval? 
49.	Can retrieval return incorrect chunks? 
50.	How does retrieval affect answer quality? 
________________________________________
Section 6 – Reranking
51.	Why are retrieved chunks reranked? 
52.	Which reranker is used? 
53.	What is the input to the reranker? 
54.	What is the output of the reranker? 
55.	Why are only Top-K chunks selected? 
56.	How does reranking improve answer quality? 
57.	Can reranking retrieve missing chunks? 
58.	What happens after reranking? 
59.	Why is reranking important? 
60.	How does reranking reduce hallucination? 
________________________________________
Section 7 – Prompt Construction
61.	What is prompt construction? 
62.	Why is prompt construction required? 
63.	What information is included in the prompt? 
64.	Does the prompt include the user question? 
65.	Does the prompt include the retrieved chunks? 
66.	Does the prompt include system instructions? 
67.	Why should prompt construction be carefully designed? 
68.	How does prompt quality affect answer quality? 
69.	Can different prompts produce different answers? 
70.	Which module receives the constructed prompt? 
________________________________________
Section 8 – Answer Generation
71.	Which LLM generates the answer? 
72.	What is the input to the LLM? 
73.	What is the output of the LLM? 
74.	Does the LLM search the database? 
75.	Does the LLM use retrieved chunks? 
76.	Does the LLM generate completely new information? 
77.	Can the LLM generate unsupported statements? 
78.	Why should answers be based only on retrieved evidence? 
79.	How is the final answer generated? 
80.	What happens after answer generation? 
________________________________________
Section 9 – Hallucination
81.	What is hallucination? 
82.	Why do hallucinations occur? 
83.	How does RAG reduce hallucinations? 
84.	Can RAG completely eliminate hallucinations? 
85.	What happens if irrelevant chunks are retrieved? 
86.	How does reranking reduce hallucinations? 
87.	How does Groundedness Assessment reduce hallucinations? 
88.	How does Evidence Highlighting reduce hallucinations? 
89.	How does Trust Score help users identify hallucinations? 
90.	Which module contributes the most to reducing hallucinations? 
________________________________________
Section 10 – Practical Implementation
91.	Which LangChain components are used to build the RAG pipeline? 
92.	How do we connect the retriever with the LLM? 
93.	How is the prompt created? 
94.	How are retrieved chunks passed to Gemma 3? 
95.	How is the final answer received? 
96.	How do we display the answer? 
97.	How do we display supporting evidence? 
98.	How do we debug incorrect answers? 
99.	How do we test the RAG pipeline? 
100.	Which module should be tested first if answer generation fails? 
________________________________________
Section 11 – Advantages
101.	What are the advantages of RAG? 
102.	Why is RAG better than an LLM alone? 
103.	Why is RAG suitable for research assistants? 
104.	How does RAG improve answer accuracy? 
105.	How does RAG improve reliability? 
106.	How does RAG reduce hallucination? 
107.	Why is RAG scalable? 
108.	Why is RAG suitable for continuously growing datasets? 
109.	Why is RAG becoming popular in industry? 
110.	How does RAG improve user trust? 
________________________________________
Section 12 – Limitations
111.	What are the limitations of RAG? 
112.	Does RAG depend on retrieval quality? 
113.	Does RAG depend on chunk quality? 
114.	Does RAG depend on embeddings? 
115.	Can poor retrieval produce poor answers? 
116.	Can RAG still hallucinate? 
117.	How does dataset quality affect RAG? 
118.	How does prompt quality affect RAG? 
119.	What improvements can be made to RAG? 
120.	Is RAG an active area of research? 
________________________________________
Section 13 – Comparisons
121.	RAG vs Fine-tuning 
122.	RAG vs ChatGPT 
123.	RAG vs Search Engines 
124.	RAG vs Traditional QA Systems 
125.	RAG vs OpenScholar 
126.	RAG vs ResearchMind 
127.	Standard RAG vs Enhanced RAG 
128.	Which approach is more suitable for ResearchMind? 
129.	Why did we choose RAG instead of fine-tuning? 
130.	Can RAG and fine-tuning be used together? 
________________________________________
Section 14 – RAG in ResearchMind
131.	How is RAG implemented in ResearchMind? 
132.	Which modules make our RAG pipeline different? 
133.	How does Section-Aware Retrieval improve RAG? 
134.	How does Hybrid Retrieval improve RAG? 
135.	How does reranking improve RAG? 
136.	How does Evidence Highlighting improve RAG? 
137.	How does Groundedness Assessment improve RAG? 
138.	How does Trust Score improve RAG? 
139.	Why do we call our system Enhanced RAG? 
140.	How does ResearchMind improve the traditional RAG architecture? 
________________________________________
Section 15 – Coding & Testing
141.	Which LangChain chain is used for RAG? 
142.	How do you connect the retriever to the LLM? 
143.	How do you build the complete RAG pipeline? 
144.	How do you test the complete RAG pipeline? 
145.	How do you debug retrieval errors? 
146.	How do you debug prompt errors? 
147.	How do you debug LLM output? 
148.	How do you verify that retrieved chunks are actually used? 
149.	Which modules should be tested individually before testing the complete RAG pipeline? 
150.	How do you validate the end-to-end system? 
________________________________________
Section 16 – Management Questions
151.	Why did you choose RAG? 
152.	Why not fine-tune Gemma 3? 
153.	Can RAG work without retrieval? 
154.	Can RAG work without an LLM? 
155.	What happens if incorrect chunks are retrieved? 
156.	Which module contributes the most to answer quality? 
157.	Which module contributes the most to reducing hallucination? 
158.	Why is your RAG called Enhanced RAG? 
159.	How is ResearchMind different from a normal RAG system? 
160.	If you redesign the complete RAG pipeline, what improvements would you make? 
MODULE 10 – EXPLAINABLE AI (XAI)
Chapter 15 – Explainable AI (XAI) in ResearchMind
________________________________________
Section 1 – Introduction
Understanding
1.	What is Explainable AI (XAI)? 
2.	Why is Explainable AI important? 
3.	What problems does Explainable AI solve? 
4.	Why is Explainable AI required in ResearchMind? 
5.	Where is Explainable AI used? 
6.	At which stage of the ResearchMind pipeline is Explainable AI applied? 
7.	What is the input to the Explainable AI module? 
8.	What is the output of the Explainable AI module? 
9.	Can ResearchMind work without Explainable AI? 
10.	What are the Explainable AI components in ResearchMind? 
________________________________________
Section 2 – Need for Explainable AI
11.	Why shouldn't users blindly trust AI-generated answers? 
12.	What is a Black Box AI system? 
13.	Why are many AI systems considered black boxes? 
14.	What challenges do black-box systems create? 
15.	Why is transparency important in AI? 
16.	Why is explainability important in research applications? 
17.	Why is explainability more important in healthcare and research than in casual chatbots? 
18.	How does Explainable AI improve user confidence? 
19.	How does Explainable AI improve decision-making? 
20.	Why is Explainable AI one of the novelties of ResearchMind? 
________________________________________
Section 3 – Explainability in ResearchMind
21.	Which Explainable AI features are included in ResearchMind? 
22.	What is Evidence Highlighting? 
23.	What is Groundedness Assessment? 
24.	What is Trust Score? 
25.	Why are these three modules introduced? 
26.	At which stage are they executed? 
27.	Which module receives the LLM output? 
28.	Does Explainable AI modify the answer? 
29.	Can Explainable AI detect unsupported statements? 
30.	Can Explainable AI improve answer reliability? 
________________________________________
Section 4 – Evidence Highlighting
31.	What is Evidence Highlighting? 
32.	Why is Evidence Highlighting required? 
33.	How does Evidence Highlighting work? 
34.	Which information is highlighted? 
35.	Does Evidence Highlighting use retrieved chunks? 
36.	Can one answer have multiple evidence sources? 
37.	Can evidence come from multiple research papers? 
38.	Does Evidence Highlighting improve transparency? 
39.	Does Evidence Highlighting improve user trust? 
40.	Where is Evidence Highlighting displayed to the user? 
________________________________________
Practical Understanding
41.	How are evidence sentences identified? 
42.	Can the system highlight exact supporting sentences? 
43.	What happens if no supporting evidence is found? 
44.	Can incorrect retrieval affect Evidence Highlighting? 
45.	Can Evidence Highlighting reduce hallucination? 
46.	Does Evidence Highlighting generate new information? 
47.	Can Evidence Highlighting improve explainability? 
48.	Can highlighted evidence include page numbers? 
49.	Can highlighted evidence include paper titles? 
50.	Why is Evidence Highlighting useful for researchers? 
________________________________________
Section 5 – Groundedness Assessment
51.	What is Groundedness Assessment? 
52.	Why is Groundedness Assessment required? 
53.	What is meant by a grounded answer? 
54.	How does Groundedness Assessment work? 
55.	What is the input to Groundedness Assessment? 
56.	What is the output? 
57.	Does it compare the generated answer with retrieved evidence? 
58.	Can unsupported statements be identified? 
59.	Can partially supported answers be detected? 
60.	Why is Groundedness important? 
________________________________________
Practical Understanding
61.	How is groundedness measured? 
62.	Can every sentence be verified separately? 
63.	What happens if one sentence has no supporting evidence? 
64.	Can Groundedness Assessment reduce hallucination? 
65.	Can Groundedness Assessment improve answer quality? 
66.	Can Groundedness Assessment improve trust? 
67.	Can it improve evaluation? 
68.	Can it improve publication quality? 
69.	What happens after Groundedness Assessment? 
70.	Can the answer still be displayed if groundedness is low? 
________________________________________
Section 6 – Trust Score
71.	What is a Trust Score? 
72.	Why is a Trust Score required? 
73.	How does a Trust Score help users? 
74.	At which stage is the Trust Score generated? 
75.	What factors influence the Trust Score? 
76.	Does retrieval quality affect the Trust Score? 
77.	Does groundedness affect the Trust Score? 
78.	Does evidence quality affect the Trust Score? 
79.	Can answer confidence affect the Trust Score? 
80.	Why should users see the Trust Score? 
________________________________________
Practical Understanding
81.	How is the Trust Score calculated? 
82.	Is the Trust Score a percentage? 
83.	Can different answers have different Trust Scores? 
84.	What does a high Trust Score indicate? 
85.	What does a low Trust Score indicate? 
86.	Can users rely only on the Trust Score? 
87.	Can the Trust Score improve decision-making? 
88.	Can incorrect retrieval reduce the Trust Score? 
89.	Can better reranking improve the Trust Score? 
90.	How should the Trust Score be displayed? 
________________________________________
Section 7 – Explainability Workflow
91.	Explain the complete Explainable AI workflow. 
92.	Which module executes first? 
93.	Which module executes after answer generation? 
94.	How does Evidence Highlighting interact with Groundedness Assessment? 
95.	How does Groundedness Assessment influence the Trust Score? 
96.	Which module produces the final output? 
97.	Can these modules run independently? 
98.	What happens if one module fails? 
99.	Which Explainable AI module contributes the most? 
100.	Draw the Explainable AI workflow. 
________________________________________
Section 8 – Advantages
101.	What are the advantages of Explainable AI? 
102.	How does Explainable AI improve transparency? 
103.	How does Explainable AI improve user trust? 
104.	How does Explainable AI improve answer quality? 
105.	How does Explainable AI improve scientific research? 
106.	Why is Explainable AI useful for students? 
107.	Why is Explainable AI useful for researchers? 
108.	How does Explainable AI reduce hallucination? 
109.	Why is Explainable AI becoming important in modern AI? 
110.	Why is Explainable AI the major novelty of ResearchMind? 
________________________________________
Section 9 – Limitations
111.	What are the limitations of Explainable AI? 
112.	Can Explainable AI guarantee correctness? 
113.	Does Explainable AI depend on retrieval quality? 
114.	Does Explainable AI depend on reranking? 
115.	Does Explainable AI depend on the LLM output? 
116.	Can incorrect evidence produce incorrect explanations? 
117.	Can Explainable AI increase response time? 
118.	Can Explainable AI increase computational cost? 
119.	How can Explainable AI be improved? 
120.	Is Explainable AI an active research area? 
________________________________________
Section 10 – Comparisons
121.	ResearchMind with XAI vs ResearchMind without XAI 
122.	OpenScholar vs ResearchMind Explainability 
123.	Traditional RAG vs Explainable RAG 
124.	Black Box AI vs Explainable AI 
125.	Explainable AI vs Interpretable AI 
126.	Explainability vs Transparency 
127.	Explainability vs Accuracy 
128.	Can Explainable AI reduce hallucination more effectively than prompt engineering? 
129.	Why did we choose Explainable AI as our novelty? 
130.	How does Explainable AI make ResearchMind different from existing research assistants? 
________________________________________
Section 11 – Practical Implementation
131.	Which Python libraries can support Explainable AI? 
132.	How is Evidence Highlighting implemented? 
133.	How is Groundedness Assessment implemented? 
134.	How is the Trust Score calculated? 
135.	How do we display highlighted evidence? 
136.	How do we display citations? 
137.	How do we display the Trust Score? 
138.	How do we test Explainable AI? 
139.	How do we debug Explainable AI modules? 
140.	How do we validate Explainable AI outputs? 
________________________________________
Section 12 – Evaluation
141.	How do we evaluate Evidence Highlighting? 
142.	How do we evaluate Groundedness? 
143.	How do we evaluate the Trust Score? 
144.	Which evaluation metrics are suitable? 
145.	How do we compare Explainable AI with traditional RAG? 
146.	How do we measure user trust? 
147.	How do we measure transparency? 
148.	How do we evaluate answer reliability? 
149.	Which experiments should be conducted? 
150.	How should Explainable AI results be presented? 
________________________________________
Section 13 – Management Questions
151.	Why did you include Explainable AI? 
152.	Why doesn't OpenScholar provide Explainable AI? 
153.	Why is Explainable AI your novelty? 
154.	Can Explainable AI eliminate hallucination? 
155.	Can users completely trust the Trust Score? 
156.	How does Evidence Highlighting improve research? 
157.	Why is Groundedness Assessment important? 
158.	How do you calculate the Trust Score? 
159.	If Explainable AI is removed, how will ResearchMind be affected? 
160.	Why should management consider this a significant research contribution? 
________________________________________
Section 14 – Critical Thinking
161.	Can Explainable AI be improved further? 
162.	Can the Trust Score be learned automatically? 
163.	Can user feedback improve Explainable AI? 
164.	Can Explainable AI be applied to image-based RAG? 
165.	Can Explainable AI be used in healthcare? 
166.	Can Explainable AI be integrated with Agentic AI? 
167.	What future research opportunities exist in Explainable AI? 
168.	How will Explainable AI evolve over the next five years? 
169.	If you redesign the Explainable AI module, what improvements would you make? 
170.	Is Explainable AI sufficient to make AI completely trustworthy? Explain your answer. 
MODULE 11 – DYNAMIC KNOWLEDGE BASE
Chapter 16 – Dynamic Research Paper Ingestion Pipeline
________________________________________
Section 1 – Introduction
Understanding
1.	What is a Dynamic Research Paper Ingestion Pipeline? 
2.	Why is a Dynamic Research Paper Ingestion Pipeline required? 
3.	What problem does it solve? 
4.	Why is this module included in ResearchMind? 
5.	At which stage of the ResearchMind pipeline does it operate? 
6.	Is this module executed during answer generation or separately? 
7.	What is the input to the ingestion pipeline? 
8.	What is the output of the ingestion pipeline? 
9.	Can ResearchMind work without this module? 
10.	Why is this module considered one of the novelties of ResearchMind? 
________________________________________
Section 2 – Need for Dynamic Ingestion
11.	Why do research papers continuously increase? 
12.	Why can't we manually update the dataset every time? 
13.	Why shouldn't we retrain the LLM whenever new papers are published? 
14.	What are the disadvantages of retraining? 
15.	Why should the knowledge base be updated automatically? 
16.	Why is a static dataset insufficient? 
17.	How does Dynamic Ingestion make ResearchMind future-ready? 
18.	Why is Dynamic Ingestion better than rebuilding the entire database? 
19.	Why is Dynamic Ingestion important for RAG systems? 
20.	Why is Dynamic Ingestion more suitable than periodic manual updates? 
________________________________________
Section 3 – Data Sources
21.	From where can new research papers be collected? 
22.	What is arXiv? 
23.	What is Semantic Scholar? 
24.	What is Crossref? 
25.	What is PubMed? 
26.	Which repositories provide open-access research papers? 
27.	Why should only trusted sources be used? 
28.	Can multiple repositories be monitored? 
29.	How does the system know which repository to check? 
30.	Can users specify their own research paper source? 
________________________________________
Section 4 – Monitoring New Papers
31.	How does the system detect newly published papers? 
32.	How often should repositories be checked? 
33.	Does the system download every paper? 
34.	How are relevant papers identified? 
35.	Can keyword filters be applied? 
36.	Can publication year be used as a filter? 
37.	Can research domains be filtered? 
38.	How are duplicate papers identified? 
39.	What happens if the same paper appears in multiple repositories? 
40.	How are duplicate downloads avoided? 
________________________________________
Section 5 – Downloading Papers
41.	How are research papers downloaded? 
42.	What file format is downloaded? 
43.	Where are downloaded papers stored? 
44.	How is download success verified? 
45.	What happens if a download fails? 
46.	How are corrupted PDF files handled? 
47.	Can metadata be downloaded before the PDF? 
48.	Can only selected papers be downloaded? 
49.	Can users approve downloaded papers manually? 
50.	What happens after downloading is complete? 
________________________________________
Section 6 – Automatic Processing
51.	What happens after a new PDF is downloaded? 
52.	Is PDF processing performed automatically? 
53.	Is Document Structure Extraction performed automatically? 
54.	Is chunking performed automatically? 
55.	Are embeddings generated automatically? 
56.	Is metadata generated automatically? 
57.	Are vectors automatically stored in ChromaDB? 
58.	Is the knowledge base updated automatically? 
59.	Is manual intervention required? 
60.	How does the complete automation process work? 
________________________________________
Section 7 – Knowledge Base Update
61.	How is the existing knowledge base updated? 
62.	Is the entire database recreated? 
63.	Are only new papers processed? 
64.	How are new embeddings added? 
65.	Can old embeddings remain unchanged? 
66.	Can existing vectors be modified? 
67.	What happens if a paper is removed? 
68.	Can outdated papers be deleted? 
69.	How does the system maintain consistency? 
70.	Why is incremental updating better than rebuilding the database? 
________________________________________
Section 8 – Memory Management
71.	Why is memory management important? 
72.	Does continuously adding papers increase storage? 
73.	How does the vector database grow over time? 
74.	Can unlimited papers be stored? 
75.	What happens when storage becomes full? 
76.	How can duplicate embeddings waste memory? 
77.	How can outdated papers affect storage? 
78.	Should old papers be archived? 
79.	How can storage usage be optimized? 
80.	Why is memory management important for large-scale deployment? 
________________________________________
Section 9 – Scheduling
81.	How often should the ingestion pipeline run? 
82.	Can it run daily? 
83.	Can it run weekly? 
84.	Can it run monthly? 
85.	Can it be triggered manually? 
86.	Can users configure the schedule? 
87.	Which scheduling tools can be used? 
88.	Can the pipeline run in the background? 
89.	What happens if the system is offline? 
90.	How can missed updates be recovered? 
________________________________________
Section 10 – Advantages
91.	What are the advantages of Dynamic Research Paper Ingestion? 
92.	How does it improve ResearchMind? 
93.	How does it reduce manual work? 
94.	Why is it more scalable? 
95.	How does it improve answer quality? 
96.	How does it improve knowledge freshness? 
97.	Why is it suitable for universities? 
98.	Why is it suitable for research organizations? 
99.	Why is it important for real-world deployment? 
100.	Why is this module a major novelty? 
________________________________________
Section 11 – Limitations
101.	What are the limitations of Dynamic Ingestion? 
102.	What happens if repositories change their APIs? 
103.	What happens if internet connectivity is unavailable? 
104.	Can incorrect papers be downloaded? 
105.	Can duplicate papers still appear? 
106.	Does this module increase computation time? 
107.	Does this module increase storage requirements? 
108.	How can these limitations be addressed? 
109.	Is Dynamic Ingestion suitable for all applications? 
110.	What future improvements can be added? 
________________________________________
Section 12 – Practical Implementation
111.	Which APIs can be used to fetch research papers? 
112.	How can the arXiv API be used? 
113.	How can the Semantic Scholar API be used? 
114.	How do we search for new papers? 
115.	How do we download PDF files programmatically? 
116.	How do we automatically trigger preprocessing? 
117.	How do we update ChromaDB? 
118.	How do we verify successful updates? 
119.	How do we test the ingestion pipeline? 
120.	How do we debug failures? 
________________________________________
Section 13 – Comparisons
121.	Manual Dataset Update vs Dynamic Ingestion 
122.	Static Dataset vs Dynamic Dataset 
123.	Retraining vs Dynamic Knowledge Base Update 
124.	Batch Update vs Incremental Update 
125.	OpenScholar Dataset vs ResearchMind Dynamic Dataset 
126.	Static Knowledge Base vs Dynamic Knowledge Base 
127.	Which approach is more suitable for ResearchMind? 
128.	Why didn't OpenScholar include Dynamic Ingestion? 
129.	Why is Dynamic Ingestion more practical? 
130.	How does Dynamic Ingestion improve RAG? 
________________________________________
Section 14 – Management Questions
131.	Why did you introduce Dynamic Ingestion? 
132.	Why not manually update the dataset? 
133.	Why not retrain the LLM? 
134.	How will ResearchMind include tomorrow's research papers? 
135.	How do you avoid downloading duplicate papers? 
136.	How do you ensure only relevant papers are added? 
137.	Does Dynamic Ingestion affect the trained LLM? 
138.	How does this module improve the project? 
139.	If this module is removed, how will ResearchMind be affected? 
140.	Why should this be considered a research contribution? 
________________________________________
Section 15 – Critical Thinking
141.	Can the ingestion pipeline learn user interests? 
142.	Can the pipeline prioritize highly cited papers? 
143.	Can the pipeline summarize papers before storing them? 
144.	Can the pipeline reject low-quality papers automatically? 
145.	Can the pipeline support multilingual research papers? 
146.	Can user feedback improve paper selection? 
147.	Can this module be used in other RAG applications? 
148.	How will this module evolve in future AI systems? 
149.	If you redesign the ingestion pipeline, what improvements would you make? 
150.	Can Dynamic Ingestion make ResearchMind a continuously evolving research assistant?
MODULE 12 – EVALUATION & PERFORMANCE ANALYSIS
Chapter 17 – Evaluation of ResearchMind
________________________________________
Section 1 – Introduction
Understanding
1.	What is system evaluation? 
2.	Why is evaluation required? 
3.	Why is evaluation important in AI projects? 
4.	Why should ResearchMind be evaluated? 
5.	What is the objective of evaluation? 
6.	At which stage of the project is evaluation performed? 
7.	What is evaluated in ResearchMind? 
8.	What are evaluation metrics? 
9.	Why are evaluation metrics important? 
10.	Can a project be considered successful without evaluation? 
________________________________________
Section 2 – Evaluation Dataset
11.	Which dataset will be used for evaluation? 
12.	Should the same dataset be used for training and evaluation? 
13.	How are evaluation questions prepared? 
14.	Who prepares the expected answers? 
15.	How many test questions should be used? 
16.	Should easy, medium, and difficult questions be included? 
17.	Should questions come from multiple research papers? 
18.	Can users create their own evaluation questions? 
19.	Why should evaluation use realistic research questions? 
20.	How do we ensure fair evaluation? 
________________________________________
Section 3 – Retrieval Evaluation
21.	What is retrieval evaluation? 
22.	Why should retrieval be evaluated separately? 
23.	What is Retrieval Accuracy? 
24.	How do we measure Retrieval Accuracy? 
25.	What is Context Recall? 
26.	What is Context Precision? 
27.	Why is Context Precision important? 
28.	Why is Context Recall important? 
29.	How do we know the correct chunks were retrieved? 
30.	How does retrieval quality affect answer generation? 
________________________________________
Section 4 – Answer Evaluation
31.	What is answer evaluation? 
32.	Why should generated answers be evaluated? 
33.	What is Answer Relevance? 
34.	How is Answer Relevance measured? 
35.	What is Answer Correctness? 
36.	How do we compare generated answers with expected answers? 
37.	Can a correct answer still be incomplete? 
38.	Can an answer be relevant but incorrect? 
39.	How do we evaluate answer completeness? 
40.	Why should answer quality be measured? 
________________________________________
Section 5 – Explainability Evaluation
41.	How do we evaluate Evidence Highlighting? 
42.	How do we verify highlighted evidence? 
43.	What is Groundedness? 
44.	How is Groundedness evaluated? 
45.	What is Faithfulness? 
46.	Why is Faithfulness important? 
47.	How do we verify that every statement is supported? 
48.	How do we evaluate the Trust Score? 
49.	How do we know Explainable AI is working correctly? 
50.	Why should explainability be evaluated separately? 
________________________________________
Section 6 – RAGAS Evaluation
51.	What is RAGAS? 
52.	What does RAGAS stand for? 
53.	Why is RAGAS used? 
54.	Which modules of ResearchMind are evaluated using RAGAS? 
55.	Is RAGAS an open-source framework? 
56.	Which programming language supports RAGAS? 
57.	Can RAGAS evaluate any RAG system? 
58.	Why did we choose RAGAS? 
59.	Can RAGAS replace manual evaluation? 
60.	How is RAGAS integrated into ResearchMind? 
________________________________________
Section 7 – RAGAS Metrics
61.	What is Context Precision? 
62.	What is Context Recall? 
63.	What is Faithfulness? 
64.	What is Answer Relevancy? 
65.	What is Answer Correctness? 
66.	Which RAGAS metrics are used in ResearchMind? 
67.	Why is Context Precision important? 
68.	Why is Faithfulness important? 
69.	Why is Answer Relevancy important? 
70.	Which metric is most important for our project? 
________________________________________
Section 8 – Performance Evaluation
71.	What is Response Time? 
72.	Why is Response Time important? 
73.	How is Response Time measured? 
74.	What is Latency? 
75.	How does retrieval affect latency? 
76.	How does reranking affect latency? 
77.	How does the LLM affect latency? 
78.	How do we reduce response time? 
79.	Why should performance be measured? 
80.	How does performance affect user experience? 
________________________________________
Section 9 – Comparative Evaluation
81.	Why should ResearchMind be compared with OpenScholar? 
82.	Which features should be compared? 
83.	How do we compare retrieval quality? 
84.	How do we compare answer quality? 
85.	How do we compare explainability? 
86.	How do we compare execution time? 
87.	How do we compare Trust Score? 
88.	How do we compare hallucination reduction? 
89.	How do we compare user satisfaction? 
90.	Why should baseline comparison be included in the project? 
________________________________________
Section 10 – User Evaluation
91.	Why should users evaluate the system? 
92.	Who are the expected users? 
93.	How do we collect user feedback? 
94.	What questions should be asked during user evaluation? 
95.	How is user satisfaction measured? 
96.	Why is user feedback important? 
97.	Can user feedback improve ResearchMind? 
98.	Should students evaluate the system? 
99.	Should faculty evaluate the system? 
100.	How do we analyse user feedback? 
________________________________________
Section 11 – Experimental Setup
101.	What hardware was used for evaluation? 
102.	What software environment was used? 
103.	Which operating system was used? 
104.	Which Python version was used? 
105.	Which libraries were used? 
106.	Which LLM was used? 
107.	Which embedding model was used? 
108.	Which vector database was used? 
109.	Why should the experimental setup be documented? 
110.	How can another researcher reproduce the experiment? 
________________________________________
Section 12 – Result Analysis
111.	How do we interpret evaluation results? 
112.	What does a high Faithfulness score indicate? 
113.	What does a low Context Precision score indicate? 
114.	What does a low Trust Score indicate? 
115.	How do we identify weaknesses in the system? 
116.	How do we identify strengths in the system? 
117.	Which module contributed the most improvement? 
118.	Which module requires further optimization? 
119.	How should results be presented in the project report? 
120.	Why is result analysis important? 
________________________________________
Section 13 – Practical Implementation
121.	How do you install RAGAS? 
122.	How do you prepare the evaluation dataset? 
123.	How do you run RAGAS? 
124.	How do you evaluate Faithfulness? 
125.	How do you evaluate Answer Relevancy? 
126.	How do you evaluate Context Precision? 
127.	How do you evaluate Context Recall? 
128.	How do you generate evaluation reports? 
129.	How do you visualize evaluation results? 
130.	How do you debug poor evaluation scores? 
________________________________________
Section 14 – Management Questions
131.	How did you prove your project works? 
132.	Why did you choose RAGAS? 
133.	Which evaluation metric is most important? 
134.	How did you compare your system with OpenScholar? 
135.	How do you know retrieval has improved? 
136.	How do you know Explainable AI has improved the system? 
137.	How do you know Hybrid Retrieval is better than BM25 alone? 
138.	Which module contributed the maximum improvement? 
139.	If evaluation results are poor, what improvements would you make? 
140.	Why should management believe your evaluation results? 
________________________________________
Section 15 – Critical Thinking
141.	Can evaluation metrics guarantee a perfect system? 
142.	Can user feedback contradict RAGAS results? 
143.	How would you evaluate the system if no benchmark dataset existed? 
144.	Can evaluation metrics be manipulated? 
145.	Which evaluation metric would you add in future? 
146.	How would you evaluate a multilingual version of ResearchMind? 
147.	How would you evaluate a larger dataset with millions of papers? 
148.	How would you evaluate future improvements? 
149.	If you redesign the evaluation framework, what changes would you make? 
150.	Why is evaluation considered as important as implementation in AI research? 
MODULE 13 – DEPLOYMENT & SYSTEM ARCHITECTURE
Chapter 18 – Deployment of ResearchMind
________________________________________
Section 1 – Introduction
Understanding
1.	What is deployment? 
2.	Why is deployment required? 
3.	Why is deployment the final stage of software development? 
4.	What is the objective of deployment? 
5.	Who will use the deployed system? 
6.	What is the difference between development and deployment? 
7.	What are the different types of deployment? 
8.	Why is deployment important for AI applications? 
9.	At which stage is ResearchMind deployed? 
10.	What is the expected output after deployment? 
________________________________________
Section 2 – System Architecture
11.	What is system architecture? 
12.	Why is system architecture important? 
13.	What are the major components of ResearchMind? 
14.	Which component acts as the frontend? 
15.	Which component acts as the backend? 
16.	Which component performs retrieval? 
17.	Which component stores the knowledge base? 
18.	Which component generates answers? 
19.	How do all components communicate? 
20.	Draw the complete deployment architecture of ResearchMind. 
________________________________________
Section 3 – Frontend
21.	What is a frontend? 
22.	Why is a frontend required? 
23.	Which frontend framework is used in ResearchMind? 
24.	Why did we choose Angular? 
25.	What are the responsibilities of the frontend? 
26.	What input does the frontend collect? 
27.	What output does the frontend display? 
28.	How are uploaded PDFs handled? 
29.	How are user questions submitted? 
30.	How are answers displayed? 
________________________________________
Section 4 – Backend
31.	What is a backend? 
32.	Why is a backend required? 
33.	Which backend framework is used? 
34.	Why did we choose FastAPI? 
35.	What are the responsibilities of the backend? 
36.	How does the backend receive user requests? 
37.	How does the backend communicate with the retrieval module? 
38.	How does the backend communicate with Gemma 3? 
39.	How does the backend send responses to the frontend? 
40.	Why is FastAPI suitable for AI applications? 
________________________________________
Section 5 – API Communication
41.	What is an API? 
42.	What does API stand for? 
43.	Why are APIs required? 
44.	How does the frontend communicate with the backend? 
45.	Which HTTP methods are commonly used? 
46.	What is a REST API? 
47.	Why is REST API used in ResearchMind? 
48.	What is a request? 
49.	What is a response? 
50.	What format is used to exchange data? 
________________________________________
Section 6 – Local LLM Deployment
51.	Why are we running Gemma 3 locally? 
52.	What is Ollama? 
53.	How does Ollama run Gemma 3? 
54.	Does the backend communicate directly with Ollama? 
55.	Can multiple models be managed by Ollama? 
56.	Can another LLM replace Gemma 3? 
57.	What are the hardware requirements? 
58.	Can Gemma 3 run without internet? 
59.	Why is local deployment suitable for student projects? 
60.	What are the limitations of local deployment? 
________________________________________
Section 7 – Database Deployment
61.	Where is ChromaDB deployed? 
62.	How is the vector database connected to FastAPI? 
63.	How are embeddings stored permanently? 
64.	How does the backend query ChromaDB? 
65.	Can multiple users access the same database? 
66.	How is the database backed up? 
67.	What happens if the database becomes corrupted? 
68.	Can ChromaDB be migrated to another server? 
69.	How is metadata stored? 
70.	How does the database support Dynamic Ingestion? 
________________________________________
Section 8 – User Management
71.	Who are the intended users of ResearchMind? 
72.	Can multiple users access the application simultaneously? 
73.	Should users log in before using the system? 
74.	How can user authentication be implemented? 
75.	Should uploaded research papers be private or shared? 
76.	Can different users maintain separate knowledge bases? 
77.	How can user activity be monitored? 
78.	What user information should be stored? 
79.	How can user privacy be protected? 
80.	How can unauthorized access be prevented? 
________________________________________
Section 9 – Deployment Options
81.	Can ResearchMind run on a personal laptop? 
82.	Can ResearchMind be deployed on a university server? 
83.	Can ResearchMind be deployed on AWS? 
84.	Can ResearchMind be deployed using Docker? 
85.	What is Docker? 
86.	Why is Docker useful? 
87.	What are the advantages of containerization? 
88.	Can Kubernetes be used? 
89.	Which deployment option is recommended for students? 
90.	Which deployment option is suitable for production? 
________________________________________
Section 10 – Performance & Scalability
91.	How does the system handle multiple users? 
92.	What happens when many users ask questions simultaneously? 
93.	How can performance be improved? 
94.	How can response time be reduced? 
95.	What factors affect scalability? 
96.	Can ResearchMind support one million research papers? 
97.	What changes are required for large-scale deployment? 
98.	How can load balancing be implemented? 
99.	Why is scalability important? 
100.	How can future growth be supported? 
________________________________________
Section 11 – Security
101.	Why is security important? 
102.	How should uploaded research papers be protected? 
103.	How should API endpoints be secured? 
104.	How can unauthorized users be blocked? 
105.	Why should HTTPS be used? 
106.	How can sensitive information be protected? 
107.	How should API keys be managed? 
108.	How can malicious file uploads be prevented? 
109.	What are common security risks in AI applications? 
110.	How can these risks be minimized? 
________________________________________
Section 12 – Practical Implementation
111.	How do you run the Angular frontend? 
112.	How do you start the FastAPI backend? 
113.	How do you start Ollama? 
114.	How do you connect FastAPI with Ollama? 
115.	How do you connect FastAPI with ChromaDB? 
116.	How do you test API endpoints? 
117.	How do you verify frontend-backend communication? 
118.	How do you debug deployment errors? 
119.	How do you package the application? 
120.	How do you prepare the application for demonstration? 
________________________________________
Section 13 – Management Questions
121.	How will users access ResearchMind? 
122.	Why did you choose Angular? 
123.	Why did you choose FastAPI? 
124.	Why did you choose Ollama instead of cloud APIs? 
125.	Why did you deploy locally? 
126.	Can your application work online? 
127.	Can multiple users use the application at the same time? 
128.	What changes are required for commercial deployment? 
129.	How will you deploy this application for a university? 
130.	If ResearchMind is deployed for thousands of users, what improvements would you make? 
________________________________________
Section 14 – Critical Thinking
131.	Can the system be converted into a web application? 
132.	Can the system be converted into a mobile application? 
133.	Can cloud deployment improve performance? 
134.	How would you deploy ResearchMind globally? 
135.	How can CI/CD be added to this project? 
136.	How can monitoring and logging be implemented? 
137.	What future deployment improvements can be added? 
138.	If you redesign the deployment architecture, what changes would you make? 
139.	How can the deployment cost be reduced? 
140.	What deployment strategy would you recommend for a real research organization?
MODULE 14 – END-TO-END PROJECT EXECUTION
Chapter 19 – Complete End-to-End ResearchMind Workflow
________________________________________
Section 1 – Complete Overview
Understanding
1.	Explain the complete workflow of ResearchMind. 
2.	What is the first step in the project? 
3.	What is the last step in the project? 
4.	Which modules are involved in the complete workflow? 
5.	What is the input to the complete system? 
6.	What is the final output? 
7.	Which module performs preprocessing? 
8.	Which module performs retrieval? 
9.	Which module generates the answer? 
10.	Which module verifies the answer? 
________________________________________
Section 2 – Dataset Preparation
11.	How are research papers collected? 
12.	From where are research papers collected? 
13.	Why are PDFs used? 
14.	Why is metadata collected? 
15.	How are duplicate papers removed? 
16.	How are papers organized? 
17.	Where are PDFs stored? 
18.	How many research papers are collected initially? 
19.	Why is the dataset prepared before system execution? 
20.	What happens after dataset preparation? 
________________________________________
Section 3 – PDF Processing
21.	What happens when a PDF enters the system? 
22.	Which library extracts the text? 
23.	Why is text extraction required? 
24.	What happens if the PDF is corrupted? 
25.	How are scanned PDFs handled? 
26.	Which information is extracted? 
27.	What happens after text extraction? 
28.	Why is clean text important? 
29.	Can images be extracted? 
30.	What is the output of this stage? 
________________________________________
Section 4 – Document Structure Extraction
31.	Why is document structure identified? 
32.	Which sections are detected? 
33.	How is section metadata generated? 
34.	Why is section metadata stored? 
35.	How does this help retrieval? 
36.	Can one paper have multiple sections? 
37.	What happens after section detection? 
38.	Which module uses this metadata? 
39.	Why is this one of the novelties? 
40.	What is the output of this stage? 
________________________________________
Section 5 – Chunking
41.	Why is chunking required? 
42.	Which chunking method is used? 
43.	What chunk size is selected? 
44.	Why is overlap required? 
45.	How many chunks are generated? 
46.	How are chunks linked to metadata? 
47.	Why are chunks stored separately? 
48.	What happens after chunking? 
49.	Which module receives the chunks? 
50.	How does chunk quality affect the project? 
________________________________________
Section 6 – Embedding Generation
51.	Why are embeddings generated? 
52.	Which embedding model is used? 
53.	How is every chunk converted into an embedding? 
54.	Does every chunk generate one embedding? 
55.	Why are vectors generated? 
56.	How are query embeddings generated? 
57.	Where are embeddings stored? 
58.	Which module receives the embeddings? 
59.	What happens after embedding generation? 
60.	How does embedding quality affect retrieval? 
________________________________________
Section 7 – ChromaDB
61.	Why is ChromaDB used? 
62.	What is stored inside ChromaDB? 
63.	Are chunks stored? 
64.	Are embeddings stored? 
65.	Is metadata stored? 
66.	How are embeddings indexed? 
67.	How does ChromaDB perform similarity search? 
68.	Can ChromaDB be updated? 
69.	What happens after storage? 
70.	Which module queries ChromaDB? 
________________________________________
Section 8 – User Question
71.	What happens when the user asks a question? 
72.	How does the frontend receive the question? 
73.	How is the question sent to the backend? 
74.	Is the query converted into an embedding? 
75.	Which embedding model is used? 
76.	Which retrieval modules receive the query? 
77.	Can different questions produce different retrieval results? 
78.	What happens after query processing? 
79.	Why is query processing important? 
80.	What is the output of this stage? 
________________________________________
Section 9 – BM25 Retrieval
81.	How does BM25 retrieve chunks? 
82.	Does BM25 use embeddings? 
83.	Does BM25 search keywords? 
84.	How are BM25 scores calculated? 
85.	How many chunks are retrieved? 
86.	What are the advantages of BM25? 
87.	What are its limitations? 
88.	Which module receives BM25 results? 
89.	What happens after BM25 retrieval? 
90.	Why is BM25 combined with Dense Retrieval? 
________________________________________
Section 10 – Dense Retrieval
91.	How does Dense Retrieval work? 
92.	How does Dense Retrieval use embeddings? 
93.	How are similarity scores calculated? 
94.	Why is cosine similarity used? 
95.	How many chunks are retrieved? 
96.	Which module receives Dense Retrieval results? 
97.	What are the advantages? 
98.	What are the limitations? 
99.	What happens after Dense Retrieval? 
100.	Why isn't Dense Retrieval sufficient alone? 
________________________________________
Section 11 – Hybrid Retrieval
101.	Why are BM25 and Dense Retrieval combined? 
102.	How are both results merged? 
103.	How are duplicate chunks removed? 
104.	How are retrieval weights applied? 
105.	How is the final candidate list prepared? 
106.	How many chunks move to reranking? 
107.	Why is Hybrid Retrieval better? 
108.	Which module receives these chunks? 
109.	What happens after Hybrid Retrieval? 
110.	Why is Hybrid Retrieval our novelty? 
________________________________________
Section 12 – Cross-Encoder Reranking
111.	Why is reranking required? 
112.	Which model performs reranking? 
113.	How are relevance scores generated? 
114.	How are chunks reordered? 
115.	How many chunks are selected? 
116.	Why are low-scoring chunks removed? 
117.	Which module receives the reranked chunks? 
118.	What happens after reranking? 
119.	Why is reranking important? 
120.	How does reranking improve answer quality? 
________________________________________
Section 13 – Prompt Construction
121.	How is the final prompt created? 
122.	What information is included? 
123.	How are retrieved chunks inserted? 
124.	How is the user question added? 
125.	How are system instructions added? 
126.	Why is prompt engineering important? 
127.	Which module receives the prompt? 
128.	Can prompt design affect answers? 
129.	What happens after prompt construction? 
130.	Why should prompts be tested? 
________________________________________
Section 14 – LLM Answer Generation
131.	Which LLM generates the answer? 
132.	Why was Gemma 3 selected? 
133.	How does Gemma 3 generate the answer? 
134.	Does Gemma 3 search the database? 
135.	Does Gemma 3 generate new knowledge? 
136.	Can Gemma 3 hallucinate? 
137.	What happens after answer generation? 
138.	Which module receives the answer? 
139.	How is the answer prepared? 
140.	Why is answer verification still required? 
________________________________________
Section 15 – Explainable AI
141.	How does Evidence Highlighting work? 
142.	How does Groundedness Assessment work? 
143.	How is the Trust Score calculated? 
144.	How is the final verified answer prepared? 
145.	Which evidence is displayed? 
146.	How are citations displayed? 
147.	What happens if groundedness is low? 
148.	Can unsupported statements be detected? 
149.	How is user trust improved? 
150.	What is displayed on the final screen? 
________________________________________
Section 16 – Dynamic Ingestion
151.	How are newly published papers detected? 
152.	How are they downloaded? 
153.	How are they processed automatically? 
154.	How are embeddings generated? 
155.	How are new vectors added to ChromaDB? 
156.	Does the LLM need retraining? 
157.	How is duplication avoided? 
158.	How does the knowledge base remain updated? 
159.	Why is this one of our novelties? 
160.	How does it improve ResearchMind? 
________________________________________
Section 17 – Complete Pipeline
161.	Explain the complete pipeline from PDF upload to answer generation. 
162.	Explain the complete pipeline from the user question to retrieval. 
163.	Explain the complete pipeline from retrieval to answer generation. 
164.	Explain the complete pipeline from answer generation to Explainable AI. 
165.	Explain the entire project in two minutes. 
166.	Explain the project in five minutes. 
167.	Explain the project in ten minutes. 
168.	Draw the complete architecture. 
169.	Draw the complete data flow diagram. 
170.	Explain how data flows through every module. 
________________________________________
Section 18 – Failure Scenarios
171.	What happens if PDF extraction fails? 
172.	What happens if chunking fails? 
173.	What happens if embedding generation fails? 
174.	What happens if ChromaDB is unavailable? 
175.	What happens if BM25 retrieves nothing? 
176.	What happens if Dense Retrieval retrieves irrelevant chunks? 
177.	What happens if Hybrid Retrieval fails? 
178.	What happens if reranking fails? 
179.	What happens if Gemma 3 is unavailable? 
180.	What happens if Explainable AI cannot verify the answer? 
________________________________________
Section 19 – Optimization
181.	Which module consumes the most time? 
182.	Which module consumes the most memory? 
183.	Which module requires GPU support? 
184.	Which module can be parallelized? 
185.	How can response time be reduced? 
186.	How can retrieval speed be improved? 
187.	How can answer quality be improved? 
188.	How can Explainable AI be improved? 
189.	How can the Dynamic Ingestion Pipeline be optimized? 
190.	How can the overall system be optimized? 
________________________________________
Section 20 – Complete Project Understanding
191.	Which module is the most important? 
192.	Which module is your biggest novelty? 
193.	Which module contributes most to answer quality? 
194.	Which module contributes most to reducing hallucination? 
195.	Which module is the most difficult to implement? 
196.	Which module can be improved in future? 
197.	If one module is removed, which one should never be removed? Why? 
198.	What is the biggest strength of ResearchMind? 
199.	What is the biggest limitation of ResearchMind? 
200.	Explain ResearchMind as if you are presenting it to an IEEE review committee.

