# robin
----THE PROJECT IS STILL IN DEVELOPMENT. CHECK THE BRANCHES FOR THE LATEST WORK----

Robin is an innovative, AI-driven e-learning platform that automatically generates adaptive, personalized curricula and transforms them into engaging video lessons. Leveraging advanced Retrieval Augmented Generation (RAG) techniques and agentic AI components, Robin aims to revolutionize digital education by dynamically tailoring learning experiences based on each user's performance and feedback.

## Project Overview
 - Robin automatically ingests and indexes educational content (e.g., PDFs, articles, 3D animations, diagrams) and uses state-of-the-art language models to:
    1. Generate Customized Curricula: Automatically build lesson plans and educational paths tailored to user needs.
    2. Create Engaging Video Lessons: Convert dynamically generated lesson scripts into high-quality video content using text-to-speech, AI-driven video generation, and integrated visual assets.
    3. Provide Adaptive Learning: Adjust subsequent lessons based on interactive quizzes and user performance, ensuring a personalized learning experience.
    4. Seamlessly Integrate Multi-Modal Content: Incorporate text, images, diagrams, and 3D animations to create rich, interactive educational materials.

### Architecture Principles

**Feature-First Organization:**
- Each major feature (`auth`, `rag`, `agents`, etc.) is self-contained
- Consistent internal structure: `*_routes.py` (API), `*_controller.py` (logic), `*_models.py` (data) etc
- Clear separation between business logic and data access

**Scalability Features:**
- Modular design allows independent development and testing of features
- Database layer abstraction for easy migration between storage solutions
- Separate `services/` for complex business operations like parallel query processing

**RAG-Specific Structure:**
- Dedicated `rag/` module for all retrieval-augmented generation functionality
- Separate `data/` directory with organized storage for raw and processed content
- Vector database operations isolated for performance optimization

## Tech Stack
  - **Backend**
      1. Frameworks: Python (FastAPI)
      2. LLM & RAG Integration: LangChain 
      3. Databases:
            1. Relational: DynamoDB for user data, curriculum metadata, and quiz scores
            2. Vector Database: FAISS for content retrieval and multi-modal embeddings
      4. Media Processing: Integration with TTS APIs (e.g., AWS Polly, Google Cloud TTS), text-to-video APIs (e.g., Synthesia, D-ID), MoviePy, and FFmpeg for video assembly
  - **Frontend**
      1. Framework: React for building a dynamic, responsive user interface
      2. Video Embedding: HTML5 video players and interactive components for quizzes and feedback 
  - **Cloud & DevOps**
      1. Storage: AWS S3 for video files, images, and other media assets
      2. Deployment: Docker for containerization and AWS (ECS) for hosting

## Project Structure

Robin follows a **feature-first architecture** designed for scalability, maintainability, and clear separation of concerns. Each major feature is organized into its own module with a consistent structure.

```
server/
├── app/ # Main application code
│ ├── auth/ # Authentication & authorization
│ │ ├── auth_routes.py # API endpoints
│ │ ├── auth_controller.py # App logic
│ │ └── auth_models.py # Data models
│ │
│ ├── rag/ # Retrieval Augmented Generation
│ │ ├── vector_store.py # Vector database operations
│ │ └── embeddings.py # Text/multi-modal embeddings
│ │
│ ├── agents/ # AI Agents for curriculum generation
│ │ ├── agents.py # Agent orchestration
│ │ └── tools.py # Agent tools and utilities
│ │
│ ├── services/ # Core business services
│ │ ├── parallel_query.py # Concurrent query processing
│ │ ├── query_llm.py # LLM interaction service
│ │ ├── narrator.py # Text-to-speech services
| | └── parallel_query.py # Concurrent query processing
│ │
│ ├── database/ # Database layer
│ │
│ ├── animation/ # Video & animation generation
│ │ └── templates/ # Animation templates
| |     |── animate_text.py
| |     |── temp.py
| |     └── test.py     
│ │
│ ├── utils/ # Shared utilities
│ │ └── helpers.py # Common helper functions
│ │
│ ├── config.py # Application environment variables configuration
│ └── main.py # FastAPI application entry point
│
├── data/ # Data storage
│ ├── PDFs/ # PDF documents for RAG
│ └── output # Stored outputs
│
├── tests/ # Test suite
├── requirements.txt # Python dependencies
└── README.md # Project documentation
```