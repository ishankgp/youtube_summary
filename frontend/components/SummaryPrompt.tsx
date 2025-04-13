"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Card } from "@/components/ui/card"
import { Loader2 } from "lucide-react"

const DEFAULT_PROMPT = `Please provide a comprehensive and structured summary of the video content with the following sections:

# Overall Summary
Provide a clear and concise 2-3 paragraph overview of the main content, including:
- The primary topic and purpose of the video
- Key messages and main takeaways
- The overall tone and style of the presentation

# Detailed Breakdown
Organize the content into logical sections based on the video's structure:
- Main topics covered
- Important concepts explained
- Step-by-step processes (if applicable)
- Key demonstrations or examples
- Technical details or specifications

# Key Points & Analysis
For each major point or topic:
- Main arguments or explanations
- Supporting evidence or examples
- Practical applications or implications
- Any unique insights or perspectives
- Connections to broader context

# Speaker/Content Analysis
If there are multiple speakers or sections:
- Individual contributions and viewpoints
- Areas of agreement or consensus
- Contrasting perspectives or debates
- Notable expertise or credentials
- Speaking style and presentation approach

# Notable Quotes & Timestamps
Include 3-5 significant quotes that capture key insights:
> "Quote text" - [Speaker Name, Timestamp]
> "Another important quote" - [Speaker Name, Timestamp]

# Additional Context
Include any relevant:
- Background information
- Related concepts or topics
- References to other works
- Resources mentioned
- Follow-up recommendations

IMPORTANT FORMATTING RULES:
1. Use markdown headers (#, ##, ###) for section titles only
2. DO NOT use any bold formatting (** **) in the content
3. DO NOT use any other markdown formatting except for:
   - Headers (#, ##, ###)
   - Bullet points (-)
   - Quote blocks (>) for Notable Quotes
4. Keep all content in regular weight text, not bold
5. Ensure timestamps are included with quotes
6. Maintain clear hierarchy in the content structure`

interface SummaryPromptProps {
  value: string
  onChange: (value: string) => void
  onProcess?: (prompt: string) => void
  disabled?: boolean
  isProcessing?: boolean
}

export default function SummaryPrompt({ 
  value, 
  onChange, 
  onProcess,
  disabled,
  isProcessing 
}: SummaryPromptProps) {
  const [localValue, setLocalValue] = useState(value || DEFAULT_PROMPT)
  const [isEdited, setIsEdited] = useState(false)

  const handleChange = (newValue: string) => {
    setLocalValue(newValue)
    setIsEdited(true)
    onChange(newValue)
  }

  const handleProcess = () => {
    if (onProcess) {
      onProcess(localValue)
    }
  }

  return (
    <div className="space-y-4">
      <div className="space-y-2">
        <label className="text-sm font-medium text-muted-foreground">
          Customize how you want the summary to be generated:
        </label>
        <Textarea
          value={localValue}
          onChange={(e) => handleChange(e.target.value)}
          disabled={disabled}
          className="min-h-[400px] font-mono text-sm"
          placeholder="Enter your custom prompt..."
        />
      </div>
      
      {isEdited && onProcess && (
        <Button 
          onClick={handleProcess}
          disabled={disabled || isProcessing}
          className="w-full"
        >
          {isProcessing ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              Regenerating Summary...
            </>
          ) : (
            'Regenerate Summary'
          )}
        </Button>
      )}
    </div>
  )
}

