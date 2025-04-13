import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs) {
  return twMerge(clsx(inputs));
}

export function extractYouTubeVideoId(url) {
  try {
    const urlObj = new URL(url);
    if (urlObj.hostname === 'www.youtube.com') {
      return urlObj.searchParams.get('v');
    } else if (urlObj.hostname === 'youtu.be') {
      return urlObj.pathname.slice(1);
    }
    return null;
  } catch {
    return null;
  }
} 