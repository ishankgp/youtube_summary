import Image from 'next/image';
import { extractYouTubeVideoId } from '@/lib/utils';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { X } from 'lucide-react';

interface YouTubeThumbnailProps {
  url: string;
  onRemove: () => void;
  isValid: boolean;
}

export function YouTubeThumbnail({ url, onRemove, isValid }: YouTubeThumbnailProps) {
  const videoId = extractYouTubeVideoId(url);
  const thumbnailUrl = videoId ? `https://img.youtube.com/vi/${videoId}/mqdefault.jpg` : null;

  return (
    <div className="relative group">
      <div className="relative rounded-lg overflow-hidden bg-slate-950/10 aspect-video">
        {thumbnailUrl ? (
          <Image
            src={thumbnailUrl}
            alt="YouTube video thumbnail"
            fill
            className="object-cover transition-transform group-hover:scale-105"
            sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
          />
        ) : (
          <div className="absolute inset-0 flex items-center justify-center">
            <span className="text-slate-500">No thumbnail available</span>
          </div>
        )}
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
        <Badge 
          variant={isValid ? "default" : "destructive"} 
          className="absolute top-2 left-2"
        >
          {isValid ? "Valid URL" : "Invalid URL"}
        </Badge>
        <Button
          variant="ghost"
          size="icon"
          className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity"
          onClick={onRemove}
        >
          <X className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
} 