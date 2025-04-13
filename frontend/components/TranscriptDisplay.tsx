"use client"

import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Loader2 } from 'lucide-react';

interface TranscriptData {
  transcript: string;
  language: string;
  translated?: boolean;
  original_transcript?: string;
}

interface TranscriptDisplayProps {
  transcripts: Record<string, TranscriptData>;
  isLoading?: boolean;
}

const TranscriptDisplay: React.FC<TranscriptDisplayProps> = ({ 
  transcripts,
  isLoading = false
}) => {
  if (isLoading) {
    return (
      <div className="flex items-center justify-center text-muted-foreground p-8">
        <Loader2 className="h-6 w-6 animate-spin mr-2" />
        <span>Fetching transcripts...</span>
      </div>
    );
  }

  if (Object.keys(transcripts).length === 0) {
    return (
      <div className="text-center text-muted-foreground p-8">
        No transcripts available yet. Process some videos to see their transcripts here.
      </div>
    );
  }

  return (
    <ScrollArea className="h-[500px] pr-4">
      {Object.entries(transcripts).map(([url, data], index) => (
        <Card key={url} className="mb-4 last:mb-0">
          <CardContent className="p-4">
            <h3 className="font-semibold mb-2 text-sm">
              Video {index + 1}: {url}
              <span className="ml-2 text-xs text-muted-foreground">
                {data.translated ? (
                  <span className="text-blue-500">
                    (Translated from {data.language})
                  </span>
                ) : (
                  <span>(Language: {data.language})</span>
                )}
              </span>
            </h3>
            <div className="whitespace-pre-wrap text-sm">
              {data.transcript}
            </div>
          </CardContent>
        </Card>
      ))}
    </ScrollArea>
  );
};

export default TranscriptDisplay;

