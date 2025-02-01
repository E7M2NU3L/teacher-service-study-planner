# RaG Application

## Overview
The RaG Application is a Django-based service designed to assist educators by creating an intelligent teacher bot. This bot leverages Retrieval-Augmented Generation (RAG) architecture, integrating Chroma Vector Database with the powerful Gemini API. The application allows users to upload PDF files, which are processed to enable efficient information retrieval and test generation.

## Features
- **PDF Upload:** Users can upload PDF files containing educational content.
- **Teacher Bot (RAG):** Utilizes Chroma Vector DB and Gemini API to provide accurate and context-aware responses.
- **Custom Test Generation:** Generate tests with customizable options such as total marks, number of questions, and difficulty levels.

## Technology Stack
- **Backend:** Django
- **Database:** Chroma Vector DB
- **API Integration:** Gemini API
- **AI Architecture:** Retrieval-Augmented Generation (RAG)

## Installation
1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd rag-application
   ```
2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```
5. **Run the server:**
   ```bash
   python manage.py runserver
   ```

## Usage
1. **Upload PDF Files:** Navigate to the upload section and select the desired PDFs.
2. **Interact with Teacher Bot:** Ask questions based on the uploaded content.
3. **Generate Tests:** Specify custom parameters like total marks, number of questions, and difficulty level to create tailored tests.

## Configuration
- **Gemini API Key:** Add your Gemini API key in the `.env` file:
  ```bash
  GEMINI_API_KEY=your_api_key_here
  ```
- **Database Settings:** Update `settings.py` if needed to configure Chroma Vector DB.

## Contributing
1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Create a Pull Request

## License
This project is licensed under the [MIT License](LICENSE).

## Contact
For any inquiries or support, please contact [Your Name] at [aemmanuel.codes@gmail.com].

