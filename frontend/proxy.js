const http = require('http');
const httpProxy = require('http-proxy');
const fs = require('fs');
const path = require('path');
const url = require('url');

// バックエンドAPIのURL（適宜書き換えてください）
const BACKEND_API = 'http://192.168.100.26:8000/api/status';

const proxy = httpProxy.createProxyServer({
  target: BACKEND_API,
  changeOrigin: true
});

// 静的ファイルのベースディレクトリ
const PUBLIC_DIR = path.join(__dirname);

const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url);
  const sanitizedPath = path.normalize(parsedUrl.pathname).replace(/^(\.\.[\/\\])+/, '');
  const pathname = path.join(PUBLIC_DIR, sanitizedPath);

  // 1. /api で始まるリクエストはバックエンドにプロキシ
  if (req.url.startsWith('/api/')) {
    proxy.web(req, res, {}, (err) => {
      console.error('Proxy error:', err);
      res.writeHead(502);
      res.end('Bad Gateway');
    });
    return;
  }

  // 2. ディレクトリリクエストは index.html にリダイレクト
  let filePath = pathname;
  if (fs.statSync(PUBLIC_DIR).isDirectory() && (req.url === '/' || req.url === '/index.html')) {
    filePath = path.join(PUBLIC_DIR, 'index.html');
  }

  // 3. ファイルの存在を確認して返す
  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404);
      res.end('File not found');
      return;
    }

    // 簡易的なMIMEタイプ判定
    const ext = path.extname(filePath).toLowerCase();
    const contentTypes = {
      '.html': 'text/html',
      '.js': 'text/javascript',
      '.css': 'text/css',
      '.json': 'application/json',
      '.png': 'image/png',
      '.jpg': 'image/jpeg',
      '.gif': 'image/gif',
    };

    res.writeHead(200, { 'Content-Type': contentTypes[ext] || 'application/octet-stream' });
    res.end(data);
  });
});

// サーバー起動
const PORT = 8080;
server.listen(PORT, () => {
  console.log(`Proxy server listening on http://localhost:${PORT}`);
});
