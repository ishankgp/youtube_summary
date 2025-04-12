# YouTube Transcript Processor

A modern web application that processes YouTube video transcripts and generates concise, well-structured summaries using AI. Built with Next.js, TypeScript, and Tailwind CSS.

## 🌟 Features

- **Multi-Video Processing**: Process multiple YouTube videos simultaneously
- **Smart URL Validation**: Automatic validation of YouTube URLs
- **Structured Summaries**: Well-organized summaries with:
  - Overall summary
  - Key points
  - Notable quotes with timestamps
  - Speaker analysis
  - Main themes and insights
- **Interactive UI**: Clean, responsive interface with dark mode support
- **Refinement Options**: Ability to refine and customize summaries
- **Copy & Export**: Easy sharing of generated summaries

## 📸 Screenshots

### URL Input and Processing
![URL Input Interface](./docs/images/url-input.png)
*Enter YouTube URLs with real-time validation and processing status*

### Transcript View
![Transcript View](./docs/images/transcript-view.png)
*View timestamped transcripts with easy navigation*

### Summary Output
![Summary Output](./docs/images/summary-output.png)
*Well-structured summary with key points and notable quotes*

### Refinement Options
![Refinement Panel](./docs/images/refinement-panel.png)
*Customize and refine the generated summaries*

## 🚀 Getting Started

### Prerequisites

- Node.js 18.x or higher
- npm or yarn
- A modern web browser

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/youtube_summary.git
cd youtube_summary
```

2. Install dependencies:
```bash
# Install frontend dependencies
cd frontend/my-app
npm install
# or
yarn install
```

3. Start the development server:
```bash
npm run dev
# or
yarn dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

## 🛠️ Tech Stack

- **Frontend**:
  - Next.js 14
  - TypeScript
  - Tailwind CSS
  - shadcn/ui components
  - Lucide React icons

## 📖 Usage

1. Enter one or more YouTube URLs in the input fields
2. Click "Process Videos" to generate summaries
3. View the generated transcripts and summaries
4. Use the refinement options to customize the summary if needed
5. Copy or export the results

## 🎨 UI Components

- **URL Input**: Clean interface for managing multiple YouTube URLs
- **Transcript View**: Displays timestamped transcripts
- **Summary Output**: Well-formatted summary with sections
- **Refinement Panel**: Tools for customizing summaries

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Next.js](https://nextjs.org/)
- UI components from [shadcn/ui](https://ui.shadcn.com/)
- Icons from [Lucide](https://lucide.dev/)

# Additional entries to consider
.env.local
.env.development.local
.env.test.local
.env.production.local
.cursor/
.history/
*.log.*
.tmp/
temp/
tmp/