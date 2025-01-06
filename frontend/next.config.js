/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'via.placeholder.com',
      }
    ],
    unoptimized: true,  // 禁用图片优化，直接使用原始图片
  },
}

module.exports = nextConfig 
