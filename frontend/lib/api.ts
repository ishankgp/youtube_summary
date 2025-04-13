import axios from 'axios';

// Add type declaration for process.env
declare global {
  namespace NodeJS {
    interface ProcessEnv {
      NEXT_PUBLIC_API_BASE_URL?: string;
      NEXT_PUBLIC_USE_MOCK_DATA?: string;
    }
  }
}

// Simplified API configuration with hardcoded values for now
// These will be overridden by environment variables at runtime
const API_BASE_URL = 'http://localhost:8001/api';

// Always use mock data for now until backend is ready
const useMockData = true;

const MAX_RETRIES = 3;
const RETRY_DELAY = 1000;

export interface APIError {
    code: string;
    message: string;
    details?: Record<string, any>;
}

export interface TranscriptRequest {
    urls: string[];
}

export interface TranscriptData {
    transcript: string;
    language: string;
    duration: number;
    translated: boolean;
    original_language?: string;
}

export interface TranscriptResponse {
    transcripts: Record<string, TranscriptData>;
    status: string;
}

export interface SummarizeRequest {
    transcripts: Record<string, string>;
    prompt: string;
}

export interface SummaryResponse {
    summary: string;
    status: string;
}

export interface RefinementRequest {
    summary: string;
    feedback: string;
}

const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

async function fetchWithRetry(url: string, options: RequestInit, retries = MAX_RETRIES): Promise<Response> {
    try {
        const response = await fetch(url, {
            ...options,
            signal: AbortSignal.timeout(30000), // 30 second timeout
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'API request failed');
        }
        
        return response;
    } catch (err) {
        const error = err as Error;
        if (retries > 0 && error.name !== 'AbortError') {
            await sleep(RETRY_DELAY);
            return fetchWithRetry(url, options, retries - 1);
        }
        throw error;
    }
}

export const api = {
    async fetchTranscripts(request: TranscriptRequest): Promise<TranscriptResponse> {
        if (useMockData) {
            // Return mock data when backend is not available
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
        }
        
        try {
            const response = await fetchWithRetry(`${API_BASE_URL}/transcripts`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(request),
            });

            const data = await response.json();
            return data;
        } catch (err) {
            const error = err as Error;
            throw new Error(error.message || 'Failed to fetch transcripts. Please try again.');
        }
    },

    async summarizeTranscripts(request: SummarizeRequest): Promise<SummaryResponse> {
        if (useMockData) {
            // Return mock data when backend is not available
            console.log('Using mock summary data');
            return {
                summary: "This is a mock summary for development purposes. The actual summary will be generated when the backend is properly connected.",
                status: "completed"
            };
        }
        
        try {
            const response = await fetchWithRetry(`${API_BASE_URL}/summarize`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(request),
            });

            const data = await response.json();
            return data;
        } catch (err) {
            const error = err as Error;
            throw new Error(error.message || 'Failed to generate summary. Please try again.');
        }
    },

    async refineSummary(request: RefinementRequest): Promise<SummaryResponse> {
        if (useMockData) {
            // Return mock data when backend is not available
            console.log('Using mock refined summary data');
            return {
                summary: "This is a mock refined summary. " + request.feedback + " has been applied to the original summary: " + request.summary,
                status: "completed"
            };
        }
        
        try {
            const response = await fetchWithRetry(`${API_BASE_URL}/refine`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(request),
            });

            const data = await response.json();
            return data;
        } catch (err) {
            const error = err as Error;
            throw new Error(error.message || 'Failed to refine summary. Please try again.');
        }
    },
};

// Basic mock data for development
export const mockTranscript = `
[00:00:00] Hello and welcome to this video about Next.js.
[00:00:05] Today we'll be discussing how to build modern web applications.
[00:00:10] Next.js is a React framework that enables server-side rendering.
[00:00:15] This can improve performance and SEO for your web applications.
[00:00:20] Let's start by setting up a new Next.js project.
[00:00:25] First, we'll run "npx create-next-app" to create our application.
[00:00:30] This will set up all the necessary files and dependencies.
[00:00:35] Next, we'll explore the folder structure of our application.
[00:00:40] The "pages" directory is where you define your routes.
[00:00:45] Each file in this directory becomes a route in your application.
`;

export const mockSummary = `
This video provides an introduction to Next.js, a React framework for building web applications with server-side rendering capabilities. 

Key points covered:
- Next.js enables server-side rendering for better performance and SEO
- Setting up a project using "npx create-next-app"
- Understanding the folder structure, particularly the "pages" directory for routing

The presenter walks through the initial setup process and explains how the pages directory works for creating routes in a Next.js application.
`;

export interface FetchTranscriptResponse {
  success: boolean;
  transcript?: string;
  error?: string;
}

export interface GenerateSummaryResponse {
  success: boolean;
  summary?: string;
  error?: string;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const USE_MOCK_DATA = process.env.NEXT_PUBLIC_USE_MOCK_DATA === 'true';

/**
 * Fetches the transcript for a YouTube video
 */
export async function fetchTranscript(videoUrl: string): Promise<FetchTranscriptResponse> {
  if (USE_MOCK_DATA) {
    console.log('Using mock transcript data');
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    return {
      success: true,
      transcript: mockTranscript
    };
  }

  try {
    const response = await fetch(`${API_URL}/transcript`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url: videoUrl }),
    });

    const data = await response.json();
    
    if (!response.ok) {
      return {
        success: false,
        error: data.error || 'Failed to fetch transcript'
      };
    }

    return {
      success: true,
      transcript: data.transcript
    };
  } catch (error) {
    console.error('Error fetching transcript:', error);
    return {
      success: false,
      error: 'Network error when fetching transcript'
    };
  }
}

/**
 * Generates a summary for the given transcript with an optional custom prompt
 */
export async function generateSummary(
  transcript: string, 
  customPrompt?: string
): Promise<GenerateSummaryResponse> {
  if (USE_MOCK_DATA) {
    console.log('Using mock summary data');
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 2000));
    return {
      success: true,
      summary: mockSummary
    };
  }

  try {
    const response = await fetch(`${API_URL}/summary`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        transcript, 
        custom_prompt: customPrompt 
      }),
    });

    const data = await response.json();
    
    if (!response.ok) {
      return {
        success: false,
        error: data.error || 'Failed to generate summary'
      };
    }

    return {
      success: true,
      summary: data.summary
    };
  } catch (error) {
    console.error('Error generating summary:', error);
    return {
      success: false,
      error: 'Network error when generating summary'
    };
  }
}

export interface ApiResponse {
  success: boolean;
  data?: unknown;
  error?: string;
}

export async function processVideo(url: string): Promise<ApiResponse> {
  try {
    const response = await axios.post('/api/process', { url });
    return {
      success: true,
      data: response.data
    };
  } catch (error) {
    if (error instanceof Error) {
      return {
        success: false,
        error: error.message
      };
    }
    return {
      success: false,
      error: 'An unknown error occurred'
    };
  }
}

export async function refineSummary(summary: string, feedback: string): Promise<ApiResponse> {
  try {
    const response = await axios.post('/api/refine', { summary, feedback });
    return {
      success: true,
      data: response.data
    };
  } catch (error) {
    if (error instanceof Error) {
      return {
        success: false,
        error: error.message
      };
    }
    return {
      success: false,
      error: 'An unknown error occurred'
    };
  }
} 