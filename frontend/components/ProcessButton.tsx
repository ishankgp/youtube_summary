"use client"

import React from 'react';
import { Button } from '@/components/ui/button';
import { Loader2, Play } from 'lucide-react';

interface ProcessButtonProps {
  onClick: () => void;
  disabled?: boolean;
}

export default function ProcessButton({ onClick, disabled }: ProcessButtonProps) {
  return (
    <div className="relative group">
      {/* Gradient blur effect */}
      <div className="absolute -inset-0.5 bg-gradient-to-r from-pink-600 to-purple-600 rounded-lg blur opacity-30 group-hover:opacity-100 transition duration-1000 group-hover:duration-200 animate-tilt"></div>
      
      <Button
        onClick={onClick}
        disabled={disabled}
        className="relative w-full flex items-center justify-center py-4 bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 rounded-lg font-semibold text-white shadow-lg shadow-indigo-500/25 hover:shadow-indigo-500/50 hover:animate-shimmer hover:-translate-y-0.5 transition-all duration-300"
      >
        <div className="absolute inset-0 bg-[linear-gradient(110deg,#000103,45%,#1e2631,55%,#000103)] opacity-20 transition-opacity duration-300 group-hover:opacity-0" />
        <span className="relative flex items-center gap-2">
          {disabled ? (
            <>
              <Loader2 className="h-5 w-5 animate-spin" />
              <span>Processing...</span>
            </>
          ) : (
            <>
              <Play className="h-5 w-5" />
              <span>Process Videos</span>
            </>
          )}
        </span>
      </Button>
    </div>
  );
}

