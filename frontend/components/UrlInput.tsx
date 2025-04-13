"use client"

import React from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Plus, Minus } from 'lucide-react';
import { Badge } from './ui/badge';
import { Card } from './ui/card';

interface URLInputProps {
  urls: string[];
  onChange: (urls: string[]) => void;
  disabled?: boolean;
}

const URLInput: React.FC<URLInputProps> = ({ urls, onChange, disabled }) => {
  const addURL = () => {
    onChange([...urls, '']);
  };

  const removeURL = (index: number) => {
    const newUrls = urls.filter((_, i) => i !== index);
    onChange(newUrls.length ? newUrls : ['']);
  };

  const updateURL = (index: number, value: string) => {
    const newUrls = [...urls];
    newUrls[index] = value;
    onChange(newUrls);
  };

  const validateUrl = (url: string) => {
    if (!url) return false;
    try {
      const urlObj = new URL(url);
      return urlObj.hostname === 'www.youtube.com' || urlObj.hostname === 'youtu.be';
    } catch {
      return false;
    }
  };

  return (
    <div className="space-y-4">
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {urls.map((url, index) => {
          const isValid = validateUrl(url);
          
          return (
            <Card 
              key={index}
              className="group relative overflow-hidden border-slate-800/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60"
            >
              <div className="p-4 space-y-3">
                <div className="relative">
                  <Input
                    type="url"
                    value={url}
                    onChange={(e) => updateURL(index, e.target.value)}
                    placeholder="Enter YouTube URL"
                    disabled={disabled}
                    className="pr-24 transition-all duration-200"
                  />
                  <div className="absolute inset-y-0 right-0 flex items-center pr-3">
                    <span className="text-sm text-muted-foreground">
                      URL {index + 1}
                    </span>
                  </div>
                </div>

                <div className="flex items-center justify-between">
                  <Button
                    variant="outline"
                    size="icon"
                    type="button"
                    onClick={() => removeURL(index)}
                    disabled={urls.length === 1 || disabled}
                    className="shrink-0 transition-all duration-200 hover:border-red-500/50 hover:text-red-500"
                  >
                    <Minus className="h-4 w-4" />
                  </Button>
                  <Badge variant={isValid ? "secondary" : "destructive"}>
                    {isValid ? "Valid" : "Invalid"}
                  </Badge>
                </div>
              </div>
            </Card>
          );
        })}
      </div>

      <Button
        type="button"
        variant="outline"
        size="sm"
        onClick={addURL}
        disabled={disabled}
        className="w-full mt-2 border-dashed border-slate-800/40 bg-background/95 hover:border-indigo-500/50 hover:text-indigo-500 transition-all duration-200"
      >
        <Plus className="h-4 w-4 mr-2" />
        Add Another URL
      </Button>
    </div>
  );
};

export default URLInput;

