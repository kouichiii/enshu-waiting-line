const http = require('http');
const httpProxy = require('http-proxy');

// プロキシ対象（バックエンドAPIのURL）
const BACKEND_API = 'http://192.168.100.26:8000/api/status';

const proxy = httpProxy.createProxyServer({ target: BACKEND_API, changeOrigin: true });

const server = http.createServer((req, res) => {
  // `/api/` に来たリクエストだけをプロキシ
  if (req.url.startsWith('/api/')) {
    proxy.web(req, res, {}, (e) => {
      res.writeHead(502);
      res.end('Bad Gateway');
    });
  } else {
    // 静的ファイル（HTMLやJS）の配信
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('Frontend server: not an API call');
  }
});

server.listen(8080, () => {
  console.log('Proxy server listening on http://localhost:8080');
});
