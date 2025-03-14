# YouTube Summary Generator 🎥 ➡️ 📝

A modern web application that generates concise, well-structured summaries from YouTube videos using Google's Gemini Pro AI. Built with Next.js 14, TypeScript, and FastAPI.

## ✨ Features

- **Smart Summarization**: Generates structured summaries with key points and meaningful quotes
- **Multi-Video Support**: Process multiple YouTube videos simultaneously
- **Language Support**: Automatic transcript extraction with multi-language support (prioritizes Hindi and English)
- **Modern UI**: Clean, accessible interface with smooth interactions and dark mode
- **Real-time Processing**: Live progress updates during summary generation
- **Interactive Refinement**: Customize and refine summaries based on feedback
- **Error Handling**: Robust handling of invalid URLs, unavailable transcripts, and API limits

## 🚀 Live Demo

[Try it out here](#) <!-- Add your Vercel deployment URL -->

## 🛠️ Tech Stack

### Frontend
- **Next.js 14**: React framework with server components
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling with consistent spacing
- **Shadcn/ui**: Modern, accessible UI components
- **Lucide Icons**: Beautiful icon set

### Backend
- **FastAPI**: High-performance Python web framework
- **Gemini Pro**: Google's advanced language model
- **youtube-transcript-api**: Reliable transcript extraction

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/ishankgp/youtube_summary.git
cd youtube_summary
```

2. Set up environment variables:
```bash
cp .env.example .env
# Add your Gemini API key to .env
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

## 🚀 Running Locally

1. Start the backend server:
```bash
python main.py
```

2. In a new terminal, start the frontend:
```bash
cd frontend/my-app
npm run dev
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser

## 🎯 Usage

1. Enter YouTube URL(s) in the input field
2. Click "Generate Summary"
3. Watch as the summary is generated in real-time
4. View the structured summary with:
   - Overall Summary: Concise overview of the video content
   - Key Points: Important takeaways and main ideas
   - Notable Quotes: Significant statements and timestamps

## 🎨 UI Features

- Clean, modern design with consistent spacing (space-y-6 for sections)
- Smooth hover effects and transitions
- Clear visual hierarchy with semantic headings
- Responsive layout for all screen sizes
- Accessible components with ARIA support
- Dark mode support
- Interactive elements with visual feedback
- Error states with helpful messages

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Google Gemini Pro](https://deepmind.google/technologies/gemini/) for AI capabilities
- [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) for transcript extraction
- [Shadcn/ui](https://ui.shadcn.com/) for beautiful UI components
- [Lucide](https://lucide.dev/) for icons

---
Made with ❤️ by [Ishan Nag](https://github.com/ishankgp)