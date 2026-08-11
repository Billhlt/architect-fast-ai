import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
    server: {
    port: 3003
  }
})
/* 配置端口号代码部分：
  server: {
    port: 3001
  }
ps：将上述代码加入到plugins: [vue()]后面即可，不加入则默认5173为端口号。


*/