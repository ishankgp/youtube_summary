// Mock API implementation
const useMockData = true;

export const api = {
  async fetchTranscripts(request) {
    console.log('Using mock transcript data');
    return {
      transcripts: {
        [request.urls[0]]: {
          transcript: "This is a mock transcript for development purposes.",
          language: "en",
          duration: 120,
          translated: false
        }
      },
      status: "completed"
    };
  },

  async summarizeTranscripts(request) {
    console.log('Using mock summary data');
    return {
      summary: "This is a mock summary for development purposes. The actual summary will be generated when the backend is properly connected.",
      status: "completed"
    };
  },

  async refineSummary(request) {
    console.log('Using mock refined summary data');
    return {
      summary: "This is a mock refined summary. " + request.feedback + " has been applied to the original summary: " + request.summary,
      status: "completed"
    };
  },
}; 