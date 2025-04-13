/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  // Ensure rewrites/redirects work properly
  trailingSlash: false,
  // Add proper asset prefix if needed
  assetPrefix: process.env.NEXT_PUBLIC_BASE_PATH || '',
  // Experimental features for better module resolution
  experimental: {
    instrumentationHook: false,
    esmExternals: 'loose'
  }
};

export default nextConfig;
