import { NextApiRequest, NextApiResponse } from 'next';
import httpProxyMiddleware from 'next-http-proxy-middleware';

// Backend API URL
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    // Get the path from the URL
    const path = req.query.path as string[];
    const targetUrl = `${API_URL}/${path.join('/')}`;
    
    // Log the proxy request (helpful for debugging)
    console.log(`Proxying request to: ${targetUrl}`);
    
    // Forward the request to the backend API
    return httpProxyMiddleware(req, res, {
      target: API_URL,
      pathRewrite: [
        {
          patternStr: '^/api/proxy',
          replaceStr: '',
        },
      ],
      changeOrigin: true,
    });
  } catch (error) {
    console.error('API proxy error:', error);
    return res.status(500).json({ error: 'Failed to proxy request to API' });
  }
}
