/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  // Ensure rewrites/redirects work properly
  trailingSlash: false,
  // Add proper asset prefix if needed
  assetPrefix: process.env.NEXT_PUBLIC_BASE_PATH || ''
};

export default nextConfig;
