"use client"

import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { CheckCircle2, AlertCircle, Loader2 } from "lucide-react"

type ProcessingStep = 'idle' | 'fetching_transcripts' | 'generating_summary' | 'regenerating_summary' | 'error' | 'success';

interface StatusIndicatorProps {
  status: ProcessingStep;
  error?: string;
}

export default function StatusIndicator({ status, error }: StatusIndicatorProps) {
  if (status === 'idle') return null;

  const getStatusConfig = () => {
    switch (status) {
      case 'fetching_transcripts':
        return {
          variant: 'default' as const,
          icon: <Loader2 className="h-4 w-4 animate-spin" />,
          title: 'Fetching Transcripts',
          description: 'Retrieving video transcripts...'
        };
      case 'generating_summary':
        return {
          variant: 'default' as const,
          icon: <Loader2 className="h-4 w-4 animate-spin" />,
          title: 'Generating Summary',
          description: 'Creating a summary from the transcripts...'
        };
      case 'regenerating_summary':
        return {
          variant: 'default' as const,
          icon: <Loader2 className="h-4 w-4 animate-spin" />,
          title: 'Regenerating Summary',
          description: 'Creating a new summary with your custom prompt...'
        };
      case 'success':
        return {
          variant: 'default' as const,
          icon: <CheckCircle2 className="h-4 w-4 text-green-500" />,
          title: 'Success',
          description: 'Processing completed successfully.'
        };
      case 'error':
        return {
          variant: 'destructive' as const,
          icon: <AlertCircle className="h-4 w-4" />,
          title: 'Error',
          description: error || 'An error occurred during processing.'
        };
      default:
        return null;
    }
  };

  const config = getStatusConfig();
  if (!config) return null;

  return (
    <Alert variant={config.variant}>
      <div className="flex items-center gap-2">
        {config.icon}
        <AlertTitle>{config.title}</AlertTitle>
      </div>
      <AlertDescription>{config.description}</AlertDescription>
    </Alert>
  );
}

