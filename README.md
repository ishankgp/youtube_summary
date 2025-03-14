# YouTube Video Summarizer

A powerful tool that generates insightful summaries from YouTube video transcripts using AI. The application supports multiple videos, automatic language detection, and summary refinement.

## Features

- Process multiple YouTube videos simultaneously
- Automatic transcript extraction and translation
- AI-powered summarization using Gemini API
- Interactive summary refinement
- Support for multiple languages (prioritizes Hindi and English)
- Modern and responsive UI built with Next.js and Tailwind CSS

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd youtube_summary
```

2. Create a `.env` file in the root directory with your Gemini API key:
```env
GEMINI_API_KEY=your_api_key_here
```

3. Install backend dependencies:
```bash
pip install -r requirements.txt
```

4. Install frontend dependencies:
```bash
cd frontend/my-app
npm install
```

## Running the Application

1. Start the backend server:
```bash
python main.py
```

2. In a new terminal, start the frontend development server:
```bash
cd frontend/my-app
npm run dev
```

3. Open your browser and navigate to `http://localhost:3000`

## Usage

1. Enter one or more YouTube URLs in the input fields
2. Customize your summarization prompt or use one of the suggested prompts
3. Click "Generate Summary" to process the videos
4. View the generated summary
5. Optionally, provide feedback to refine the summary

## API Endpoints

- `POST /api/summarize`: Generate summary for provided YouTube URLs
- `POST /api/refine`: Refine an existing summary based on feedback

## Technologies Used

### Backend
- FastAPI
- youtube-transcript-api
- Google Generative AI (Gemini)
- Python-dotenv

### Frontend
- Next.js 14
- TypeScript
- Tailwind CSS
- Shadcn/ui components
- Lucide icons

## Error Handling

The application handles various error scenarios:
- Invalid YouTube URLs
- Unavailable transcripts
- Language translation issues
- API rate limits
- Network errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 