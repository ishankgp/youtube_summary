"use client"

import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { 
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { 
  RefreshCw, 
  Copy, 
  Check, 
  Download,
  MessageSquarePlus,
  X,
  CopyCheck,
  BookOpen,
  Wrench,
  Lightbulb,
  Quote,
  Link,
  Video
} from 'lucide-react';

interface SummaryOutputProps {
  summary: string;
  prompt: string;
  onRefine: (feedback: string) => Promise<void>;
  disabled?: boolean;
  onPromptChange: (value: string) => void;
  isLoading: boolean;
}

const sectionIcons: Record<string, React.ReactNode> = {
  'Overall Summary': <MessageSquarePlus className="h-4 w-4" />,
  'Key Points': <BookOpen className="h-4 w-4" />,
  'Main Arguments': <Lightbulb className="h-4 w-4" />,
  'Technical Details': <Wrench className="h-4 w-4" />,
  'Notable Quotes': <Quote className="h-4 w-4" />,
  'Cross-References': <Link className="h-4 w-4" />,
  'Video List': <Video className="h-4 w-4" />,
};

const convertTimestampToSeconds = (timestamp: string): number => {
  const parts = timestamp.split(':').reverse();
  let seconds = 0;
  if (parts.length >= 1) seconds += parseInt(parts[0]); // seconds
  if (parts.length >= 2) seconds += parseInt(parts[1]) * 60; // minutes
  if (parts.length >= 3) seconds += parseInt(parts[2]) * 3600; // hours
  return seconds;
};

const extractVideoId = (url: string): string | null => {
  const patterns = [
    /(?:v=|\/)([0-9A-Za-z_-]{11}).*/, // youtube.com/watch?v=ID
    /(?:youtu\.be\/)([0-9A-Za-z_-]{11})/, // youtu.be/ID
    /(?:embed\/)([0-9A-Za-z_-]{11})/, // youtube.com/embed/ID
  ];
  
  for (const pattern of patterns) {
    const match = url.match(pattern);
    if (match) return match[1];
  }
  return null;
};

export default function SummaryOutput({
  summary,
  prompt,
  onRefine,
  disabled,
  onPromptChange,
  isLoading,
}: SummaryOutputProps) {
  const [feedback, setFeedback] = useState('');
  const [isRefining, setIsRefining] = useState(false);
  const [copied, setCopied] = useState(false);
  const [showRefinement, setShowRefinement] = useState(false);

  const handleRefine = async () => {
    if (!feedback.trim()) return;
    
    setIsRefining(true);
    try {
      await onRefine(feedback);
      setFeedback('');
      setShowRefinement(false);
    } catch (error) {
      console.error('Error refining summary:', error);
    } finally {
      setIsRefining(false);
    }
  };

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(summary);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy text:', err);
    }
  };

  const handleExport = () => {
    try {
    const blob = new Blob([summary], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'summary.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Failed to export text:', err);
    }
  };

  const processContent = (content: string, type: 'regular' | 'quote' | 'bullet' | 'video-list') => {
    const lines = content.split('\n').filter(line => line.trim());
    
    switch (type) {
      case 'video-list':
        return (
          <ul className="space-y-2">
            {lines.map((line, i) => {
              const match = line.match(/Video (\d+): (.+)/);
              if (!match) return null;
              const [_, number, title] = match;
              return (
                <li 
                  key={`video-${i}`}
                  className="flex items-center gap-2 text-sm text-muted-foreground/80 hover:text-muted-foreground transition-colors duration-300"
                >
                  <Video className="h-3.5 w-3.5 text-primary/60" />
                  <span className="font-medium">{title}</span>
                </li>
              );
            })}
          </ul>
        );

      case 'quote':
        return (
          <div className="grid gap-4">
            {lines.map((line, i) => {
              let cleanedQuote = line.trim();
              if (cleanedQuote.startsWith('>')) {
                cleanedQuote = cleanedQuote.substring(1).trim();
              }
              
              let quote = cleanedQuote;
              let videoTitle = '';
              let timestamp = '';
              let videoId = '';
              
              // Extract video title and timestamp
              const dashIndex = cleanedQuote.lastIndexOf(' - ');
              if (dashIndex > 0) {
                quote = cleanedQuote.substring(0, dashIndex).trim();
                const attrParts = cleanedQuote.substring(dashIndex + 2).split(',').map(s => s.trim());
                if (attrParts.length > 0) {
                  const fullVideoTitle = attrParts[0];
                  timestamp = attrParts[1] || '';
                  
                  // Extract video ID from the title if it contains a URL
                  const urlMatch = fullVideoTitle.match(/(https?:\/\/[^\s]+)/);
                  if (urlMatch) {
                    const url = urlMatch[1];
                    videoId = extractVideoId(url) || '';
                    videoTitle = fullVideoTitle.replace(url, '').trim();
                  } else {
                    // If no URL in title, try to extract video ID from any URL-like pattern
                    const idMatch = fullVideoTitle.match(/([a-zA-Z0-9_-]{11})/);
                    if (idMatch) {
                      videoId = idMatch[1];
                      videoTitle = fullVideoTitle;
                    } else {
                      videoTitle = fullVideoTitle;
                    }
                  }
                }
              }
              
              quote = quote.replace(/^["']|["']$/g, '');
              
              // Convert timestamp to seconds for the URL
              const timestampSeconds = timestamp ? convertTimestampToSeconds(timestamp) : 0;
              
              return (
                <div 
                  key={`quote-${i}`} 
                  className="bg-slate-950/10 rounded-lg overflow-hidden"
                >
                  <div className="p-4 space-y-3">
                    {/* Quote Text */}
                    <div className="relative">
                      <Quote className="absolute -left-3 top-0 h-5 w-5 text-primary/50" />
                      <p className="text-muted-foreground/90 italic leading-relaxed pl-6">
                        &ldquo;{quote}&rdquo;
                      </p>
                    </div>
                    
                    {/* Attribution */}
                    <div className="flex items-center justify-between mt-3 pt-3 border-t border-slate-200/5">
                      {/* Video Title */}
                      <div className="flex items-center gap-2 text-sm text-muted-foreground/80">
                        <Video className="h-4 w-4 text-primary/60" />
                        <span className="font-medium truncate max-w-[300px]">
                          {videoId ? (
                            <a 
                              href={`https://www.youtube.com/watch?v=${videoId}`}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="hover:text-primary/90 transition-colors duration-200"
                            >
                              {videoTitle}
                            </a>
                          ) : (
                            videoTitle
                          )}
                        </span>
                      </div>
                      
                      {/* Timestamp */}
                      {timestamp && videoId && (
                        <a 
                          href={`https://www.youtube.com/watch?v=${videoId}&t=${timestampSeconds}`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center gap-2 text-xs px-3 py-1.5 rounded-full bg-primary/10 hover:bg-primary/20 text-primary hover:text-primary/90 transition-all duration-200 font-medium"
                        >
                          <span className="font-mono">{timestamp}</span>
                          <Link className="h-3.5 w-3.5" />
                        </a>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        );

      case 'bullet':
        return (
          <ul className="space-y-3">
            {lines.map((item, i) => {
              const bulletText = item.replace(/^[-*#]\s*/, '');
              const indentLevel = (item.match(/^\s*/) || [''])[0].length / 2;
              
              // Check if it's a subheading (starts with ## or ###)
              const isSubheading = item.trim().startsWith('##');
              const subheadingLevel = (item.match(/^#+\s*/) || [''])[0].length - 1;
              
              if (isSubheading) {
                return (
                  <li 
                    key={`bullet-${i}`}
                    className={`
                      ${i > 0 ? 'mt-6' : ''}
                      ${subheadingLevel > 2 ? 'mt-4' : ''}
                    `}
                    style={{ marginLeft: `${(indentLevel) * 1.25}rem` }}
                  >
                    <h4 className={`
                      font-medium
                      tracking-tight 
                      text-muted-foreground/90
                      border-b 
                      border-primary/10 
                      pb-1
                      mb-3
                      inline-block
                      group-hover:border-primary/20 
                      transition-colors 
                      duration-300
                      ${subheadingLevel > 2 ? 'text-sm' : 'text-base'}
                    `}>
                      {bulletText}
                    </h4>
                  </li>
                );
              }

              const isSegment = bulletText.includes(':') && !bulletText.includes('.');
              
              return (
                <li 
                  key={`bullet-${i}`}
                  className={`
                    text-muted-foreground/90
                    hover:text-foreground/90
                    transition-colors
                    duration-300
                    pl-2
                    ${isSegment ? 'font-medium' : 'font-normal'}
                  `}
                  style={{ marginLeft: `${(indentLevel) * 1.25}rem` }}
                >
                  <div className="flex items-start gap-2">
                    <span className="inline-block w-1.5 h-1.5 rounded-full bg-primary/30 mt-2 flex-shrink-0" />
                    <span>{bulletText}</span>
                  </div>
                </li>
              );
            })}
          </ul>
        );
      
      default:
        return lines.map((line, i) => {
          // Check if it's a heading
          if (line.trim().startsWith('#')) {
            const headingLevel = (line.match(/^#+/) || [''])[0].length;
            const headingText = line.replace(/^#+\s*/, '');
            const headingIcon = sectionIcons[headingText];
            
            const HeadingComponent = `h${headingLevel}` as keyof JSX.IntrinsicElements;
            
            return (
              <HeadingComponent 
                key={`heading-${i}`}
                className={`
                  group
                  flex 
                  items-center 
                  gap-2
                  ${headingLevel === 1 ? 'text-2xl font-bold mb-6 pb-2 border-b-2' : ''}
                  ${headingLevel === 2 ? 'text-xl font-semibold mb-4 mt-8 pb-1 border-b' : ''}
                  ${headingLevel === 3 ? 'text-lg font-medium mb-3 mt-6' : ''}
                  ${headingLevel > 3 ? 'text-base font-medium mb-2 mt-4' : ''}
                  border-primary/10
                  group-hover:border-primary/20
                  transition-colors
                  duration-300
                `}
              >
                {headingIcon && (
                  <span className="text-primary/60 group-hover:text-primary/80 transition-colors duration-300">
                    {headingIcon}
                  </span>
                )}
                {headingText}
              </HeadingComponent>
            );
          }
          
          return (
            <p 
              key={`text-${i}`}
              className={`
                text-muted-foreground/90
                leading-relaxed
                ${i > 0 ? 'mt-4' : ''}
                hover:text-foreground/90
                transition-colors
                duration-300
                rounded-lg
                py-2
                ${line.length > 100 ? 'text-justify' : ''}
              `}
            >
              {line}
            </p>
          );
        });
    }
  };

  const renderSection = (content: string) => {
    const sections = content.split(/(?=# )/g);
    
    return sections.map((section, i) => {
      const lines = section.split('\n');
      const firstLine = lines[0];
      
      // Skip empty sections
      if (!firstLine?.trim()) return null;
      
      // Determine section type and content
      let sectionType: 'regular' | 'quote' | 'bullet' | 'video-list' = 'regular';
      let sectionContent = section;
      
      // Check for quotes section
      if (firstLine.toLowerCase().includes('notable quotes') || firstLine.toLowerCase().includes('quotes')) {
        sectionType = 'quote';
        // Extract quotes, skipping the header
        const quotes = lines.slice(1)
          .filter(line => line.trim())
          .map(line => {
            // If line doesn't start with >, add it
            return line.trim().startsWith('>') ? line : `> ${line}`;
          })
          .join('\n');
        sectionContent = quotes;
      }
      // Check for bullet point sections
      else if (
        firstLine.toLowerCase().includes('key points') ||
        firstLine.toLowerCase().includes('arguments') ||
        firstLine.toLowerCase().includes('details') ||
        firstLine.toLowerCase().includes('applications') ||
        firstLine.toLowerCase().includes('references')
      ) {
        sectionType = 'bullet';
      }
      // Check for video list section
      else if (firstLine.toLowerCase().includes('video list')) {
        sectionType = 'video-list';
      }
      
      return (
        <div 
          key={`section-${i}`}
          className={`
            rounded-lg
            ${firstLine.startsWith('# ') ? 'bg-primary/5 p-4' : ''}
            ${firstLine.startsWith('## Key Points') ? 'bg-primary/[0.03] p-3.5' : ''}
            ${sectionType === 'quote' ? 'mt-4' : ''}
          `}
        >
          {processContent(firstLine, 'regular')}
          {sectionContent !== firstLine && (
            <div className="mt-4">
              {processContent(sectionContent, sectionType)}
            </div>
          )}
        </div>
      );
    });
  };

  return (
    <Card className="p-4 space-y-4">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold">Summary</h2>
        <TooltipProvider>
          <Tooltip>
            <TooltipTrigger asChild>
              <Button
                variant="ghost"
                size="icon"
                className="h-8 w-8"
                onClick={handleCopy}
                disabled={!summary || isLoading}
              >
                <Copy className="h-4 w-4" />
              </Button>
            </TooltipTrigger>
            <TooltipContent>
              <p>Copy to clipboard</p>
            </TooltipContent>
          </Tooltip>
        </TooltipProvider>
      </div>
      <Textarea
        value={summary}
        onChange={(e) => onPromptChange(e.target.value)}
        placeholder="Summary will appear here..."
        className="min-h-[200px] resize-none"
        readOnly={isLoading}
      />
    </Card>
  );
}
