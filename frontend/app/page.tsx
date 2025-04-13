"use client"

import { useState } from "react"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import Layout from "../components/Layout"
import UrlInput from "../components/UrlInput"
import ProcessButton from "../components/ProcessButton"
import TranscriptDisplay from "../components/TranscriptDisplay"
import SummaryPrompt from "../components/SummaryPrompt"
import SummaryOutput from "../components/SummaryOutput"
import StatusIndicator from "../components/StatusIndicator"
import { api, TranscriptData } from "../lib/api"

type ProcessingStep = 'idle' | 'fetching_transcripts' | 'generating_summary' | 'regenerating_summary' | 'error' | 'success';

export default function Home() {
  const [activeTab, setActiveTab] = useState('transcript')
  const [urls, setUrls] = useState<string[]>([''])
  const [prompt, setPrompt] = useState('')
  const [summary, setSummary] = useState('')
  const [transcripts, setTranscripts] = useState<Record<string, TranscriptData>>({})
  const [status, setStatus] = useState<ProcessingStep>('idle')
  const [error, setError] = useState('')

  const handleProcess = async () => {
    const validUrls = urls.filter(url => url.trim());
    if (validUrls.length === 0) {
      setError('Please enter at least one valid YouTube URL')
      return
    }

    // Step 1: Fetch Transcripts
    setStatus('fetching_transcripts')
    setError('')
    setTranscripts({})
    setSummary('')

    try {
      const transcriptResponse = await api.fetchTranscripts({ urls: validUrls });
      const processedTranscripts: Record<string, TranscriptData> = {};
      
      // Process each transcript to ensure it matches our expected format
      Object.entries(transcriptResponse.transcripts).forEach(([url, data]) => {
        processedTranscripts[url] = {
          transcript: data.transcript || '',
          language: data.language || 'en',
          duration: data.duration || 0,
          translated: data.translated || false,
          original_language: data.original_language
        };
      });
      
      setTranscripts(processedTranscripts);
      setActiveTab('transcript')

      // Step 2: Generate Summary
      await generateSummary(processedTranscripts);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
      setStatus('error')
    }
  }

  const generateSummary = async (transcriptData: Record<string, TranscriptData>) => {
    setStatus('generating_summary')
    
    try {
      // Convert transcripts to the format expected by the summarize endpoint
      const transcriptsForSummary = Object.entries(transcriptData).reduce(
        (acc, [url, data]) => ({
          ...acc,
          [url]: data.transcript
        }), 
        {}
      );

      const summaryResponse = await api.summarizeTranscripts({
        transcripts: transcriptsForSummary,
        prompt: prompt || "Create a concise summary highlighting the main points and key takeaways",
      });

      setSummary(summaryResponse.summary)
      setStatus('success')
      setActiveTab('summary')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
      setStatus('error')
    }
  }

  const handleRegenerateSummary = async (newPrompt: string) => {
    if (!Object.keys(transcripts).length) {
      setError('No transcripts available to summarize')
      return
    }

    setStatus('regenerating_summary')
    setError('')
    setPrompt(newPrompt)

    try {
      await generateSummary(transcripts);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
      setStatus('error')
    }
  }

  const handleRefinement = async (feedback: string) => {
    if (!summary) {
      setError('No summary to refine')
      return
    }

    setStatus('generating_summary')
    setError('')

    try {
      const response = await api.refineSummary({
        summary,
        feedback,
      })

      setSummary(response.summary)
      setStatus('success')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
      setStatus('error')
    }
  }

  const isProcessing = status === 'fetching_transcripts' || 
                      status === 'generating_summary' || 
                      status === 'regenerating_summary';

  return (
    <Layout>
      <Card className="mb-8 relative overflow-hidden border border-slate-800/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <CardHeader>
          <CardTitle className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-500 to-pink-500">
            YouTube Transcript Processor
          </CardTitle>
          <CardDescription className="text-muted-foreground/80">
            Enter YouTube URLs to process and summarize transcripts
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <UrlInput 
            urls={urls} 
            onChange={setUrls} 
            disabled={isProcessing} 
          />
          <ProcessButton 
            onClick={handleProcess} 
            disabled={isProcessing} 
          />
        </CardContent>
      </Card>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="mb-8">
        <TabsList className="grid w-full grid-cols-2 mb-4">
          <TabsTrigger value="transcript">
            Transcript {status === 'fetching_transcripts' && '(Loading...)'}
          </TabsTrigger>
          <TabsTrigger value="summary">
            Summary {(status === 'generating_summary' || status === 'regenerating_summary') && '(Generating...)'}
          </TabsTrigger>
        </TabsList>
        <TabsContent value="transcript">
          <Card className="relative overflow-hidden border border-slate-800/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
            <CardHeader>
              <CardTitle className="text-xl font-semibold">Transcript</CardTitle>
            </CardHeader>
            <CardContent>
              <TranscriptDisplay 
                transcripts={transcripts} 
                isLoading={status === 'fetching_transcripts'}
              />
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="summary">
          <Card className="relative overflow-hidden border border-slate-800/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
            <CardHeader>
              <CardTitle className="text-xl font-semibold">Summary</CardTitle>
            </CardHeader>
            <CardContent>
              {summary ? (
                <SummaryOutput 
                  summary={summary} 
                  prompt={prompt}
                  onRefine={handleRefinement}
                  disabled={isProcessing} 
                />
              ) : (
                <SummaryPrompt 
                  value={prompt}
                  onChange={setPrompt}
                  onProcess={handleRegenerateSummary}
                  disabled={isProcessing}
                  isProcessing={status === 'generating_summary' || status === 'regenerating_summary'}
                />
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
      <StatusIndicator status={status} error={error} />
    </Layout>
  )
}
