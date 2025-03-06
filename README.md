# robin
Robin is an innovative, AI-driven e-learning platform that automatically generates adaptive, personalized curricula and transforms them into engaging video lessons. Leveraging advanced Retrieval Augmented Generation (RAG) techniques and agentic AI components, Robin aims to revolutionize digital education by dynamically tailoring learning experiences based on each user’s performance and feedback.

Project Overview
 - Robin automatically ingests and indexes educational content (e.g., PDFs, articles, 3D animations, diagrams) and uses state-of-the-art language models to:
    1. Generate Customized Curricula: Automatically build lesson plans and educational paths tailored to user needs.
    2. Create Engaging Video Lessons: Convert dynamically generated lesson scripts into high-quality video content using text-to-speech, AI-driven video generation, and integrated visual assets.
    3. Provide Adaptive Learning: Adjust subsequent lessons based on interactive quizzes and user performance, ensuring a personalized learning experience.
    4. Seamlessly Integrate Multi-Modal Content: Incorporate text, images, diagrams, and 3D animations to create rich, interactive educational materials.

Tech Stack
  - Backend
      1. Frameworks: Python (FastAPI)
      2. LLM & RAG Integration: LangChain (Might be switched to LlamaIndex or similar frameworks)
      3. Task Queue: AWS SQS for asynchronous processing
      4. Databases:
            1. Relational: DynamoDB for user data, curriculum metadata, and quiz scores
            2. Vector Database: FAISS for content retrieval and multi-modal embeddings
      5. Media Processing: Integration with TTS APIs (e.g., AWS Polly, Google Cloud TTS), text-to-video APIs (e.g., Synthesia, D-ID), MoviePy, and FFmpeg for video assembly
  - Frontend
      1. Framework: React for building a dynamic, responsive user interface
      2. Video Embedding: HTML5 video players and interactive components for quizzes and feedback
  - Cloud & DevOps
      1. Storage: AWS S3 / Google Cloud Storage for video files, images, and other media assets
      2. Monitoring & Logging: AWS Cloudwatch Alarms
      3. Deployment: Docker for containerization and cloud provider (AWS) for hosting
