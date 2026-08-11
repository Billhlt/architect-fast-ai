
const express = require('express');
const { spawn } = require('child_process');
const path = require('path');
const cors = require('cors');

const app = express();
const PORT = 3000;

// 中间件
app.use(cors());
app.use(express.json());

// 处理搜索词的路由
app.post('/process-search-term', (req, res) => {
  const { searchTerm } = req.body;

  if (!searchTerm) {
    return res.status(400).json({ error: '未提供搜索词' });
  }

  // 调用Python脚本
  const pythonScriptPath = path.join(__dirname, 'llm 拆解搜索词.py');
  const python = spawn('python', [pythonScriptPath, searchTerm]);

  let result = '';
  let error = '';

  python.stdout.on('data', (data) => {
    result += data.toString();
  });

  python.stderr.on('data', (data) => {
    error += data.toString();
  });

  python.on('close', (code) => {
    if (code !== 0) {
      return res.status(500).json({ error: `Python脚本执行错误: ${error}` });
    }

    res.json({ result: result.trim() });
  });
});

app.listen(PORT, () => {
  console.log(`服务器运行在 http://localhost:${PORT}`);
});
