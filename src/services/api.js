//该文件为前端的接口部分，如果是后端传到前端的api，该代码中的对应的函数可直接在vue文件中调用
const SPRINGAI_URL = 'http://localhost:8081'
const PYTHON_URL = 'http://localhost:8000'
export const chatAPI = {
  // 发送聊天消息
  // 异步发送消息
  async sendMessage(data, chatId) {
    try {
      // 创建URL对象
      const url = new URL(`${SPRINGAI_URL}/ai/chat`)
      // 如果有chatId，则添加到URL参数中
      if (chatId) {
        url.searchParams.append('chatId', chatId)
      }
      
      // 发送POST请求
      const response = await fetch(url, {
        method: 'POST',
        body: data instanceof FormData ? data : 
          new URLSearchParams({ prompt: data })
      })

      // 如果响应状态码不是200，则抛出错误
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      // 返回响应体读取器
      return response.body.getReader()
    } catch (error) {
      // 打印错误信息
      console.error('API Error:', error)
      // 抛出错误
      throw error
    }
  },

  // 获取聊天历史列表
  async getChatHistory(type = 'chat') {  // 添加类型参数
    try {
      const response = await fetch(`${SPRINGAI_URL}/ai/history/${type}`)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const chatIds = await response.json()
      // 转换为前端需要的格式
      return chatIds.map(id => ({
        id,
        title: type === 'pdf' ? `PDF对话 ${id.slice(-6)}` : 
               type === 'service' ? `咨询 ${id.slice(-6)}` :
               `对话 ${id.slice(-6)}`
      }))
    } catch (error) {
      console.error('API Error:', error)
      return []
    }
  },

  // 获取特定对话的消息历史
  async getChatMessages(chatId, type = 'chat') {  // 添加类型参数
    try {
      const response = await fetch(`${SPRINGAI_URL}/ai/history/${type}/${chatId}`)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const messages = await response.json()
      // 添加时间戳
      return messages.map(msg => ({
        ...msg,
        timestamp: new Date() // 由于后端没有提供时间戳，这里临时使用当前时间
      }))
    } catch (error) {
      console.error('API Error:', error)
      return []
    }
  },

} 


import axios from 'axios';

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:8002', // 你的FastAPI服务器地址
  timeout: 5000,
  // headers: {
  //   'Content-Type': 'application/json',
  // },
});

// 发送Vue数据到后端
export const sendVueData = (content) => {
  return api.post('/api/vue-data', content, {
    headers: {
      'Content-Type': 'text/plain'
    }
  });
};

// 获取总结内容
export const getSummary = () => {
  return api.get('/api/summary');
};

// 获取图片内容
export const getPicsUrls = () => {
  return api.get('/api/pics');
};

// // 获取词语位置
// export const getWordPosition = () => {
//   return api.get('/api/wordposition');
// };
