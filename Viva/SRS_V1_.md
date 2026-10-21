 
 
 
Software Requirements    Specification
 
 
 
for
 
 
 
ResearchNexusAI
 
 An Explainable Research Paper Assistant using Hybrid Domain-Based Knowledge Strategy, Hybrid Retrieval, Enhanced Retrieval-Augmented Generation (RAG), and Explainable AI

Version 1.0

 Prepared by 
24BD1A05AY  24BD1A05BH 24BD1A05BF 24BD1A05BN
        24BD1A0538
  
 
          Keshav Memorial Institute of Technology,       Department of Computer Science   and   Engineering. 
 
 
02-08-2026
Table of Contents
1. Introduction
   1.1 Purpose
   1.2 Scope
   1.3 Definitions, Acronyms, and Abbreviations
   1.4 References
   1.5 Document Overview

2. Overall Description
   2.1 Product Perspective
   2.2 Product Functions
   2.3 User Classes and Characteristics
   2.4 Operating Environment
   2.5 Design and Implementation Constraints
   2.6 User Documentation
   2.7 Assumptions and Dependencies

3. External Interface Requirements
   3.1 User Interface
   3.2 Hardware Interface
   3.3 Software Interface
   3.4 Communication Interface

4. System Features
   4.1 User Authentication
   4.2 Dashboard
   4.3 Research Domain Management
   4.4 Hybrid Search & Retrieval
   4.5 Dynamic Data Ingestion
   4.6 AI Research Assistant
   4.7 Explainable AI
   4.8 Research Workspace
   4.9 Literature Review Builder
   4.10 Notebook
   4.11 Project Management
   4.12 Paper Library
   4.13 Analytics
   4.14 Notifications
   4.15 Global Search

5. Other Nonfunctional Requirements
   5.1 Performance Requirements
   5.2 Safety Requirements
   5.3 Security Requirements
   5.4 Software Quality Attributes
   5.5 Business Rules

6. Other Requirements
   6.1 Software Requirements
   6.2 Hardware Requirements

Appendix A: Glossary
Appendix B: Analysis Models
Appendix C: To Be Determined List
Revision History
Version	Date	Author(s)	Description
1.0	02-Aug-2026	Project Team	Initial IEEE SRS Draft







Chapter 1 – Introduction
1.1 Purpose
The purpose of this Software Requirements Specification (SRS) is to define the functional and non-functional requirements for ResearchNexusAI, an Explainable Research Paper Assistant that integrates a Hybrid Domain-Based Knowledge Strategy, Hybrid Retrieval, Enhanced Retrieval-Augmented Generation (RAG), and Explainable Artificial Intelligence (XAI). This document serves as a formal agreement between stakeholders by describing the expected functionality, system behavior, interfaces, constraints, and quality requirements of the proposed system.
The SRS provides a foundation for system design, implementation, testing, deployment, and future maintenance. It ensures that developers, project supervisors, evaluators, and end users have a common understanding of the objectives and capabilities of ResearchNexusAI.

1.2 Scope
ResearchNexusAI is a web-based AI-powered research assistant designed to support researchers, students, faculty members, and professionals in discovering, understanding, organizing, and analyzing scientific literature. The system combines a curated local knowledge base with dynamic retrieval from trusted academic repositories using a Hybrid Domain-Based Knowledge Strategy.
The application employs Hybrid Retrieval by combining keyword-based search (BM25) and semantic vector search to improve retrieval accuracy. Retrieved research papers are processed through an Enhanced Retrieval-Augmented Generation (RAG) pipeline to generate evidence-based responses. Explainable AI techniques provide transparency by presenting supporting papers, citations, retrieved sections, confidence scores, and evidence used during answer generation.
In addition to research question answering, ResearchNexusAI supports paper summarization, literature review generation, research paper comparison, project organization, note-taking, and personal research workspace management.



1.3 Definitions, Acronyms, and Abbreviations
The following definitions, acronyms, and abbreviations are used throughout this Software Requirements Specification.
Term	Definition
AI	Artificial Intelligence
API	Application Programming Interface
BM25	A probabilistic ranking algorithm used for keyword-based information retrieval
ChromaDB	A vector database used for storing semantic embeddings and performing similarity search
Embedding	A numerical vector representation of text used for semantic search
Enhanced RAG	An improved Retrieval-Augmented Generation framework that combines retrieved evidence with Large Language Models to generate accurate responses
FastAPI	A high-performance Python framework for building RESTful APIs
Hybrid Retrieval	A retrieval strategy that combines keyword-based search (BM25) and semantic vector search
Knowledge Base	A collection of processed research papers, metadata, and embeddings used for information retrieval
LLM	Large Language Model
PostgreSQL	A relational database used to store structured metadata and user information
RAG	Retrieval-Augmented Generation
RRF	Reciprocal Rank Fusion, an algorithm used to combine multiple ranked retrieval results
Semantic Chunking	Dividing research papers into meaningful sections while preserving contextual information
SRS	Software Requirements Specification
UI	User Interface
XAI	Explainable Artificial Intelligence



1.4 References
The requirements specified in this document are based on the following standards, research papers, and technical resources.
Standards
The requirements specified in this document are based on the following standards, research papers, and technical resources.
[1] IEEE Std 830-1998, IEEE Recommended Practice for Software Requirements Specifications.
[2] ISO/IEC/IEEE 29148:2018, Systems and Software Engineering — Life Cycle Processes — Requirements Engineering.
Research Papers
[3] Base Paper for ResearchNexusAI (Complete IEEE citation will be added.)
[4] Lewis, P., et al., Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks, NeurIPS, 2020.
[5] PaperQA – Research paper/tool referenced in the Literature Survey for scientific question answering. (Complete IEEE citation will be added.)
[6] OpenScholar – Research paper on retrieval-augmented language models for scientific literature synthesis. (Complete IEEE citation will be added.)
[7] Additional research papers included in the Literature Survey.
Technical Documentation
[8] React Documentation
[9] FastAPI Documentation
[10] PostgreSQL Documentation
[11] ChromaDB Documentation
[12] LlamaIndex Documentation
[13] PyMuPDF Documentation
[14] Google Gemini API Documentation
1.5 Document Overview
This Software Requirements Specification is organized into six major sections.
●	Chapter 1 introduces the purpose, scope, terminology, references, and organization of the document.
●	Chapter 2 provides an overview of ResearchNexusAI, including its architecture, major functions, user classes, operating environment, constraints, assumptions, and dependencies.
●	Chapter 3 describes the external interfaces of the system, including user, hardware, software, and communication interfaces.
●	Chapter 4 specifies the functional requirements of ResearchNexusAI by describing the major system features and expected behavior.
●	Chapter 5 defines the non-functional requirements, including performance, security, reliability, scalability, usability, and business rules.
●	Chapter 6 presents the software and hardware requirements necessary for the implementation and deployment of ResearchNexusAI.
The appendices provide a glossary of technical terms, supporting analysis models such as UML and DFD diagrams, and a list of future enhancements that are beyond the scope of the current implementation.





















Chapter 2: Overall Description
2.1 Product Perspective
ResearchNexusAI is a web-based AI-powered research assistant designed to support researchers throughout the scientific research process. It integrates Hybrid Domain-Based Knowledge Strategy, Hybrid Retrieval, Enhanced Retrieval-Augmented Generation (RAG), and Explainable Artificial Intelligence (XAI) to provide transparent and evidence-based research assistance.
The system follows a modular two-phase architecture consisting of an Offline Knowledge Base Preparation Phase and an Online Research Query Processing Phase. During the offline phase, research papers are collected from trusted academic repositories, processed, semantically chunked, embedded, and indexed to build a searchable knowledge base. During the online phase, user queries are analyzed and processed through a Hybrid Retrieval pipeline that combines keyword-based retrieval and semantic vector search. Retrieved information is then used by the Enhanced RAG module to generate context-aware responses supported by citations and explainable evidence.
ResearchNexusAI operates as an independent web application while integrating with external academic repositories such as arXiv, PubMed Central (PMC), AGRIS, NASA ADS, and OpenAlex for dynamic research paper acquisition.

2.2 Product Functions
ResearchNexusAI provides a comprehensive set of features to assist users in discovering, understanding, organizing, and analyzing scientific literature. The major functions of the system include:
●	User registration, authentication, and profile management.
●	Dashboard for accessing research activities, projects, and analytics.
●	Research domain selection and management.
●	Hybrid search using BM25 keyword retrieval and semantic vector search.
●	Dynamic acquisition of research papers from trusted academic repositories.
●	AI-powered research assistance for question answering, paper summarization, paper comparison, concept explanation, and literature review generation.
●	Explainable AI that presents supporting papers, retrieved evidence, citations, retrieval scores, and confidence information.
●	Research workspace for managing projects, notes, bookmarks, and saved papers.
●	Personal paper library with organization and reading status management.
●	Analytics for monitoring research progress and user activities.
●	Notification system for research updates and reminders.
●	Global search for quick access to papers, projects, notes, and workspace resources.
2.3 User Classes and Characteristics
ResearchNexusAI is intended for users involved in academic and scientific research. The primary user classes are described below.
Researchers
Researchers use the system to search scientific literature, compare research papers, generate literature reviews, identify research gaps, and manage research projects. They require advanced search capabilities and evidence-based AI responses.
Students
Students use the system to understand research concepts, summarize scientific papers, explore related work, and organize study materials. The interface should be simple and intuitive for users with varying levels of research experience.
Faculty Members
Faculty members utilize ResearchNexusAI to support teaching, supervise research projects, evaluate literature, and guide students in academic research.
Administrator
The administrator manages the system by maintaining research domains, monitoring system performance, managing datasets, supervising user accounts, and ensuring proper operation of the knowledge base.

2.4 Operating Environment
ResearchNexusAI is developed as a web-based application that operates across multiple platforms.
Client Environment
●	Modern web browsers (Google Chrome, Microsoft Edge, Mozilla Firefox, Safari)
●	Windows, Linux, or macOS
●	Stable internet connection

Server Environment
●	Python 3.11+
●	FastAPI
●	PostgreSQL
●	ChromaDB
●	PyMuPDF
●	LlamaIndex
●	Sentence Transformers
●	Gemini 2.5 Flash API
The application may be deployed on local servers or cloud platforms such as Vercel (frontend) and cloud-based backend hosting services.

2.5 Design and Implementation Constraints
The design and implementation of ResearchNexusAI are subject to the following constraints:
●	Only trusted academic repositories are used for dynamic research paper acquisition.
●	Research papers should preferably be open-access PDF documents.
●	AI-generated responses are limited by the quality and availability of retrieved research papers.
●	External APIs such as Gemini and academic repositories require internet connectivity and may impose rate limits.
●	Semantic retrieval depends on the quality of generated embeddings and indexed document chunks.
●	The system currently processes research papers written in English.
●	Hardware limitations may affect document processing speed for large research collections.

2.6 User Documentation
The following documentation will be provided to support users and administrators:
●	User Manual
●	Installation Guide
●	Administrator Guide
●	API Documentation
●	ResearchNexusAI User Guide
●	Troubleshooting Guide
●	Frequently Asked Questions (FAQ)
These documents assist users in installation, configuration, system usage, troubleshooting, and maintenance.

2.7 Assumptions and Dependencies
The successful operation of ResearchNexusAI depends on the following assumptions and external dependencies:
Assumptions
●	Users have access to a stable internet connection.
●	Research papers obtained from external repositories are authentic and publicly accessible.
●	Users possess basic knowledge of research paper searching and scientific literature.
Dependencies
●	Availability of external academic repositories (arXiv, PubMed Central, AGRIS, NASA ADS, OpenAlex).
●	Availability of the Gemini 2.5 Flash API.
●	Proper functioning of PostgreSQL and ChromaDB databases.
●	Availability of third-party libraries such as PyMuPDF, LlamaIndex, Sentence Transformers, and FastAPI.
●	Compatibility with supported web browsers and operating systems.














Chapter 3: External Interface Requirements
3.1 User Interface
ResearchNexusAI provides a web-based graphical user interface (GUI) designed to support researchers throughout the research workflow. The interface is responsive, intuitive, and accessible through modern web browsers on desktop and laptop devices.
The major user interface components include:
●	Login and Registration Page: Allows users to securely register, log in, and manage their accounts.
●	Dashboard: Displays research domains, recent activities, research projects, saved papers, and analytics.
●	Research Search Interface: Enables users to enter natural language queries and browse research papers using Hybrid Retrieval.
●	AI Research Workspace: Displays AI-generated responses, supporting research papers, retrieved citations, confidence scores, and Explainable AI information.
●	Literature Review Builder: Allows users to generate, edit, and organize literature reviews.
●	Notebook: Provides facilities for creating and managing research notes linked to papers and projects.
●	Paper Library: Displays bookmarked and saved research papers organized into collections.
●	Project Management Interface: Enables users to create, organize, and manage multiple research projects.
●	Analytics Dashboard: Presents research statistics, reading progress, and user activity.
●	Notification Panel: Displays reminders, research updates, and important system notifications.
The user interface is implemented using React.js, TypeScript, Tailwind CSS, and Vite to provide a modern, responsive, and interactive user experience.

3.2 Hardware Interface
ResearchNexusAI does not require specialized hardware and operates using standard computing devices connected to the internet.
The hardware interfaces include:
Client Hardware
●	Desktop Computer or Laptop
●	Keyboard and Mouse
●	Display Monitor
●	Internet Connectivity
Server Hardware
●	Multi-core Processor
●	Minimum 8 GB RAM
●	SSD Storage
●	Network Interface
Optional GPU acceleration may be used during document processing and embedding generation to improve processing speed but is not mandatory for normal system operation.

3.3 Software Interface
ResearchNexusAI interacts with several software components, databases, AI models, and external academic repositories.
Operating System
●	Windows 10/11
●	Linux
Backend Framework
●	FastAPI
Frontend Technologies
●	React.js
●	TypeScript
●	Tailwind CSS
●	Vite
Databases
●	PostgreSQL (Metadata Storage)
●	ChromaDB (Vector Database)
AI and Machine Learning Components
●	PyMuPDF (PDF Text Extraction)
●	LlamaIndex (Document Processing and Semantic Chunking)
●	Sentence Transformers (Embedding Generation)
●	BAAI/bge-base-en-v1.5 (Embedding Model)
●	BM25 (Keyword Retrieval)
●	Reciprocal Rank Fusion (RRF) (Result Fusion)
●	BAAI/bge-reranker-base (Cross-Encoder Re-ranking)
●	Gemini 2.5 Flash API (Enhanced RAG Response Generation)
External Academic Repositories
●	arXiv
●	PubMed Central (PMC)
●	AGRIS
●	NASA ADS
●	OpenAlex
These software interfaces enable document processing, Hybrid Retrieval, AI-powered response generation, dynamic research paper acquisition, and knowledge base management.
3.4 Communication Interface
ResearchNexusAI communicates with users, databases, AI services, and external repositories through secure network communication.
The communication interfaces include:
●	HTTPS Protocol: Used for secure communication between the client application and the backend server.
●	RESTful APIs: Used for communication between the React frontend and the FastAPI backend.
●	Gemini API: Used for AI-powered response generation through the Enhanced Retrieval-Augmented Generation (RAG) pipeline.
●	Academic Repository APIs: Used to retrieve research papers dynamically from arXiv, PubMed Central (PMC), AGRIS, NASA ADS, and OpenAlex.
●	Database Communication: FastAPI communicates with PostgreSQL for metadata management and ChromaDB for semantic vector retrieval.
●	JSON Data Format: Used for exchanging structured data between frontend, backend, databases, and external services.
All communication involving user authentication, research data, and AI-generated responses is performed over secure encrypted connections to ensure confidentiality and data integrity.
Chapter 4: System Features
4.1 User Authentication
Description
The User Authentication feature provides secure access to ResearchNexusAI by allowing users to create accounts, log in, and manage their profiles. Authentication ensures that user-specific information such as projects, saved papers, notes, and research history is securely maintained.
Functional Requirements
●	The system shall allow new users to register using valid credentials.
●	The system shall authenticate registered users before granting access.
●	The system shall securely manage user sessions.
●	The system shall allow users to update their profile information.
●	The system shall restrict unauthorized access to protected resources.

4.2 Dashboard
Description
The Dashboard serves as the primary workspace after user login. It provides quick access to research domains, recent activities, projects, saved papers, analytics, and notifications.
Functional Requirements
●	The system shall display recently accessed research activities.
●	The system shall provide shortcuts to research projects and saved papers.
●	The system shall display research statistics and analytics.
●	The system shall provide navigation to all major system modules.


4.3 Research Domain Management
Description
ResearchNexusAI organizes research papers into multiple scientific domains. Users can browse domain-specific collections, while the administrator manages domain repositories and updates the knowledge base.
Functional Requirements
●	The system shall organize research papers into predefined domains.
●	The system shall allow users to browse available research domains.
●	The system shall support both local and dynamically acquired domains.
●	The administrator shall manage domain-specific datasets.

4.4 Hybrid Search & Retrieval
Description
ResearchNexusAI uses a Hybrid Retrieval mechanism that combines keyword-based retrieval (BM25) and semantic vector search to improve the relevance and accuracy of retrieved research papers.
Functional Requirements
●	The system shall accept natural language queries.
●	The system shall perform keyword-based retrieval using BM25.
●	The system shall perform semantic vector retrieval.
●	The system shall combine retrieval results using Reciprocal Rank Fusion (RRF).
●	The system shall apply cross-encoder re-ranking before generating responses.

4.5 Dynamic Data Ingestion
Description
When relevant research papers are unavailable in the local knowledge base, the system automatically retrieves papers from trusted academic repositories and incorporates them into the knowledge base.
Functional Requirements
●	The system shall retrieve research papers from supported repositories.
●	The system shall extract metadata and document content.
●	The system shall preprocess newly acquired research papers.
●	The system shall generate semantic embeddings.
●	The system shall update the knowledge base automatically.

4.6 AI Research Assistant
Description
The AI Research Assistant generates evidence-based responses using the Enhanced Retrieval-Augmented Generation (RAG) framework. It assists users in understanding scientific literature through intelligent question answering and summarization.
Functional Requirements
●	The system shall answer research-related questions.
●	The system shall summarize research papers.
●	The system shall compare multiple research papers.
●	The system shall explain scientific concepts.
●	The system shall generate literature review content based on retrieved evidence.

4.7 Explainable AI
Description
The Explainable AI module improves transparency by presenting the evidence used during response generation. Users can understand how the final answer was produced.
Functional Requirements
●	The system shall display retrieved research papers.
●	The system shall present supporting document sections.
●	The system shall provide citation mapping.
●	The system shall display retrieval confidence information.
●	The system shall explain the reasoning behind generated responses.

4.8 Research Workspace
Description
The Research Workspace enables users to organize research activities within a centralized environment. Users can access AI responses, saved papers, projects, notes, and research history.
Functional Requirements
●	The system shall store research sessions.
●	The system shall allow users to organize research materials.
●	The system shall maintain research history.
●	The system shall support bookmarking and paper organization.

4.9 Literature Review Builder
Description
The Literature Review Builder assists users in preparing structured literature reviews by analyzing multiple research papers and organizing supporting references.
Functional Requirements
●	The system shall generate literature review drafts.
●	The system shall compare related research papers.
●	The system shall identify common research themes.
●	The system shall assist in identifying research gaps.
●	The system shall include citations in generated literature reviews.

4.10 Notebook
Description
The Notebook provides a personal environment for creating and organizing research notes associated with papers and projects.
Functional Requirements
●	The system shall allow users to create notes.
●	The system shall edit existing notes.
●	The system shall associate notes with research papers.
●	The system shall organize notes within projects.

4.11 Project Management
Description
Project Management enables users to organize research work into multiple independent projects for efficient management of papers, notes, and literature reviews.
Functional Requirements
●	The system shall allow users to create projects.
●	The system shall allow users to rename and delete projects.
●	The system shall organize papers and notes within projects.
●	The system shall maintain project-specific research history.

4.12 Paper Library
Description
The Paper Library maintains a personal repository of bookmarked and saved research papers for future reference.
Functional Requirements
●	The system shall allow users to save research papers.
●	The system shall organize papers into collections.
●	The system shall maintain reading status.
●	The system shall support paper bookmarking.


4.13 Analytics
Description
The Analytics module provides statistical insights into user research activities and system usage.
Functional Requirements
●	The system shall display reading progress.
●	The system shall summarize research activities.
●	The system shall display project statistics.
●	The system shall generate research usage reports.

4.14 Notifications
Description
The Notification module informs users about research updates, saved papers, project changes, and other important activities.
Functional Requirements
●	The system shall notify users about project updates.
●	The system shall notify users when new research papers are added.
●	The system shall display reminders for research activities.
●	The system shall maintain notification history.

4.15 Global Search
Description
The Global Search feature provides a unified search mechanism that allows users to quickly locate papers, projects, notes, literature reviews, and other resources from anywhere within the application.
Functional Requirements
●	The system shall provide a universal search interface.
●	The system shall search across papers, notes, projects, and literature reviews.
●	The system shall display categorized search results.
●	The system shall support fast navigation to selected resources.





















Chapter 5: Other Nonfunctional Requirements
5.1 Performance Requirements
ResearchNexusAI shall provide efficient retrieval and response generation to support a smooth research experience. The system should process user queries with minimal latency while maintaining retrieval accuracy. The Hybrid Retrieval pipeline shall efficiently combine keyword-based and semantic search to identify relevant research papers before AI response generation.
The system should support concurrent user requests without significant degradation in performance. Document preprocessing, semantic chunking, and embedding generation should be optimized to efficiently process large collections of research papers. The application should also support incremental updates to the knowledge base without interrupting normal system operation.

5.2 Safety Requirements
ResearchNexusAI is intended for research assistance and does not make autonomous decisions on behalf of users. AI-generated responses are intended to assist users in understanding scientific literature and should not be considered authoritative without verification.
The system shall preserve the integrity of research data during document processing, storage, and retrieval. Automatic data ingestion shall only retrieve documents from trusted academic repositories to reduce the risk of processing unreliable or malicious content. Backup and recovery mechanisms should be available to prevent accidental data loss.

5.3 Security Requirements
ResearchNexusAI shall implement appropriate security mechanisms to protect user information and research data.
The system shall:
●	Authenticate users before granting access to protected resources.
●	Store user credentials securely using industry-standard password hashing techniques.
●	Restrict unauthorized access to user accounts, projects, notes, and saved research papers.
●	Use secure communication protocols (HTTPS) for all client-server communication.
●	Protect sensitive configuration information, including API keys and database credentials.
●	Validate all user inputs to reduce security risks such as injection attacks and unauthorized data modification.
5.4 Software Quality Attributes
Reliability
The system shall operate consistently with minimal failures during normal usage. Retrieved research papers and AI-generated responses shall be based on available evidence from trusted academic sources.
Availability
ResearchNexusAI should remain available whenever users need to perform research-related activities. The system should support continuous access to locally stored research papers even when dynamic repositories are temporarily unavailable.
Scalability
The system shall support future expansion by allowing additional research domains, larger document collections, and increasing numbers of users without requiring major architectural modifications.
Maintainability
The software shall follow a modular architecture in which individual components, such as document processing, retrieval, AI services, and databases, can be updated or replaced independently with minimal impact on the overall system.
Usability
The application shall provide an intuitive and responsive user interface that enables users to efficiently search, organize, and analyze research papers with minimal training.
Accuracy
The Hybrid Retrieval mechanism shall prioritize highly relevant research papers using keyword retrieval, semantic retrieval, result fusion, and re-ranking. AI-generated responses shall be grounded in retrieved evidence and supported by appropriate citations whenever possible.
Explainability
The system shall improve transparency by displaying retrieved research papers, supporting document sections, citation mapping, confidence information, and reasoning summaries that explain how AI-generated responses were produced.

5.5 Business Rules
The following business rules govern the operation of ResearchNexusAI:
●	The system shall prioritize the local knowledge base before initiating dynamic retrieval from external academic repositories.
●	Dynamic paper acquisition shall be performed only when relevant information is unavailable or insufficient in the local knowledge base.
●	Only trusted academic repositories such as arXiv, PubMed Central (PMC), AGRIS, NASA ADS, and OpenAlex shall be used for automatic research paper acquisition.
●	Newly acquired research papers shall undergo metadata extraction, document preprocessing, semantic chunking, embedding generation, and indexing before becoming available for search.
●	AI-generated responses shall be based on retrieved research evidence rather than unsupported model generation.
●	Explainable AI information, including supporting papers and citations, shall accompany AI-generated responses whenever applicable.
●	Users shall be responsible for verifying AI-generated content before using it in academic publications or research work.










Chapter 6: Other Requirements
6.1 Software Requirements
ResearchNexusAI requires the following software components for development, deployment, and execution. These technologies support document processing, Hybrid Retrieval, Enhanced Retrieval-Augmented Generation (RAG), Explainable AI, database management, and web application development.
Operating System
The system shall support the following operating systems for development and deployment:
●	Windows 10 or Windows 11
●	Linux (Ubuntu or equivalent)
Programming Language
●	Python 3.11 or later
Frontend Technologies
The web-based user interface shall be developed using:
●	React.js
●	TypeScript
●	Tailwind CSS
●	Vite
Backend Framework
The backend services shall be implemented using:
●	FastAPI
Database Management Systems
The application shall use two databases:
●	PostgreSQL for storing structured data such as user accounts, research paper metadata, projects, notes, and application data.
●	ChromaDB for storing semantic embeddings and supporting vector similarity search.
AI and Machine Learning Components
The AI pipeline shall use the following tools and models:
●	PyMuPDF for PDF text extraction.
●	LlamaIndex for document processing and semantic chunking.
●	Sentence Transformers for embedding generation.
●	BAAI/bge-base-en-v1.5 as the semantic embedding model.
●	BM25 for keyword-based retrieval.
●	Reciprocal Rank Fusion (RRF) for combining retrieval results.
●	BAAI/bge-reranker-base for cross-encoder re-ranking.
●	Gemini 2.5 Flash API for Retrieval-Augmented Generation (RAG) and AI-powered response generation.
Development Tools
The following tools shall be used during development and testing:
●	Visual Studio Code
●	Git
●	GitHub
●	Postman

6.2 Hardware Requirements
The following hardware configuration is recommended for developing and deploying ResearchNexusAI.
Development System

                Component	    Minimum Requirement
Processor	Intel Core i5(10th Gen)/AMD Ryzen 5 or equivalent
RAM	8 GB
Storage	256 GB SSD
Internet	Stable broadband connection
GPU	Optional
Recommended Development System

                Component	    Minimum Requirement
Processor	Intel Core i7(12th Gen or above )/AMD Ryzen 7
RAM	16 GB or higher
Storage	512 GB SSD or higher
Internet	High-Speed broadband connection
GPU	NVIDIA GPU with CUDA support (optional)
Server Requirements
The backend server should provide sufficient computational resources to support concurrent users, document processing, database operations, and AI-powered query processing.
Recommended server configuration:
●	Quad-core processor or higher.
●	Minimum 8 GB RAM.
●	SSD-based storage.
●	Stable internet connection.
●	Secure HTTPS-enabled hosting environment.
Client Requirements
End users require:
●	Desktop or laptop computer.
●	Modern web browser (Google Chrome, Microsoft Edge, Mozilla Firefox, or Safari).
●	Stable internet connection.
●	No specialized hardware is required for normal system usage.

Appendix A: Glossary
This appendix defines the important technical terms, abbreviations, and acronyms used throughout the Software Requirements Specification.
Term	Definition
AI	Artificial Intelligence
RAG	Retrieval-Augmented Generation, where retrieved documents are used to generate grounded responses.
Enhanced RAG	An extended RAG pipeline incorporating Hybrid Retrieval, reranking, citation generation, and Explainable AI.
Hybrid Retrieval	Retrieval approach combining keyword search (BM25) and semantic vector search.
BM25	A probabilistic ranking algorithm used for keyword-based document retrieval.
Semantic Search	Retrieval based on vector embeddings representing semantic meaning.
Embedding	Numerical vector representation of text used for similarity search.
ChromaDB	Vector database used for storing document embeddings.
PostgreSQL	Relational database used for storing structured metadata and application data.
Metadata	Descriptive information about research papers such as title, authors, DOI, publication year, and repository.
Chunk	A semantically meaningful section of a research paper used for retrieval.
Cross Encoder	Deep learning reranking model that improves retrieval quality by evaluating query-document relevance.
Reciprocal Rank Fusion (RRF)	Ranking algorithm used to combine results from multiple retrieval methods.
Explainable AI (XAI)	AI techniques that provide evidence, citations, confidence scores, and reasoning behind generated responses.
LLM	Large Language Model used for natural language understanding and generation.
Gemini 2.5 Flash	Google's generative AI model used for answer generation within the Enhanced RAG pipeline.
API	Application Programming Interface.
DOI	Digital Object Identifier uniquely identifying scholarly publications.
Knowledge Base	Collection of indexed research papers stored locally for retrieval.
Dynamic Data Ingestion	Automatic retrieval and indexing of research papers from external academic repositories.
Workspace	User area for managing projects, notes, saved papers, and literature reviews.
SRS	Software Requirements Specification.
UML	Unified Modeling Language.
DFD	Data Flow Diagram.
ER Diagram	Entity Relationship Diagram.



Appendix B: Analysis Models
The following analysis models were prepared during the system design phase to describe the architecture, workflow, data movement, and software structure of ResearchNexusAI.
 
B.1 System Workflow Diagram
Illustrates the complete end-to-end workflow of ResearchNexusAI, including offline knowledge base preparation, dynamic data ingestion, Hybrid Retrieval, Enhanced RAG, Explainable AI, and workspace management.
Illustrates the complete end-to-end workflow of ResearchNexusAI, including offline knowledge base preparation, dynamic data ingestion, Hybrid Retrieval, Enhanced RAG, Explainable AI, and workspace management.
B.2 System Architecture Diagram
Represents the layered architecture consisting of:
●	Presentation Layer
●	Application Layer
●	AI Processing Layer
●	Storage Layer
●	External Academic Repositories
 
B.3 Use Case Diagram
Describes interactions between users and ResearchNexusAI, including:
●	User Authentication
●	Research Paper Search
●	Hybrid Retrieval
●	AI Question Answering
●	Literature Review
●	Workspace Management
●	Project Management
●	 Notes and Bookmarks

B.4 Data Flow Diagram (DFD)
Includes:
●	DFD Level 0 (Context Diagram)
●	DFD Level 1 (Core Retrieval and Data Processing Pipeline)
These diagrams illustrate data movement among users, application modules, databases, AI services, and external repositories.
DFD Level 0 (Context Diagram)


DFD Level 1 (Core Retrieval and Data Processing Pipeline)

 







B.5 Database Design
Includes:
Relational Database Schema (PostgreSQL)
Stores:
●	Users
●	Projects
●	Notes
●	Saved Papers
●	Metadata
●	Search History
Vector Database Schema (ChromaDB)
Stores:
●	Document embeddings
●	Semantic vectors
●	Chunk identifiers
Entity Relationship Diagram
Illustrates relationships among:
●	Users
●	Projects
●	Papers
●	Chunks
●	Authors
●	Notes
●	Saved Papers
●	Literature Reviews
●	Search History




 


B.6 Module Diagram
Illustrates subsystem decomposition, including:
●	User Management
●	Dashboard
●	Search Module
●	AI Assistant
●	Knowledge Base
●	Research Workspace
●	Analytics
●	Notifications
 

B.7 Sequence Diagram
Represents the sequence of interactions during research query processing, including:
●	User request
●	Query preprocessing
●	Hybrid Retrieval
●	BM25 search
●	Semantic retrieval
●	RRF
●	Cross-Encoder reranking
●	Gemini 2.5 Flash response generation
●	Explainable AI
●	Workspace storage




 






B.8 User Interface Wireframes
Includes visual designs for:
●	Login Page
●	Dashboard
●	Research Search Interface
●	AI Chat Workspace
●	Literature Review Builder
●	Notes and Project Workspace




















Appendix C: To Be Determined (TBD) List
The following items represent planned enhancements or features that are outside the scope of the current implementation but may be incorporated in future versions of ResearchNexusAI.
ID	Future Enhancement	Status
TBD-01	Multi-user collaborative research workspace	Future Work
TBD-02	Citation export in BibTeX, RIS, APA, IEEE, and MLA formats	Future Work
TBD-03	Automatic systematic literature review generation	Future Work
TBD-04	Knowledge Graph-based retrieval (GraphRAG)	Future Work
TBD-05	Multi-modal document understanding (figures, tables, equations)	Future Work
TBD-06	Local LLM deployment for offline inference	Future Work
TBD-07	Personalized recommendation engine for research papers	Future Work
TBD-08	Voice-based research assistant	Future Work
TBD-09	Mobile application support	Future Work
TBD-10	Integration with institutional digital libraries	Future Work
TBD-11	Real-time collaborative annotations and shared projects	Future Work
TBD-12	Research trend visualization and citation network analysis	Future Work

