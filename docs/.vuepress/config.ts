import { defineUserConfig } from 'vuepress'
import { defaultTheme } from '@vuepress/theme-default'
import { MarkdownOptions } from '@vuepress/markdown'

const markdownOptions: MarkdownOptions = {
  headers: {
    level: [2, 3, 4, 5],
  },
}

export default defineUserConfig({
  lang: 'zh-CN',
  title: '控制面板',
  description: '控制面板',
  base: '/control-panel-webapp/',


  markdown: markdownOptions,
  theme: defaultTheme({
    // 在这里进行配置
    repo: 'https://github.com/HenryZhuHR/control-panel-webapp',
    sidebarDepth: 4, // 设置根据页面标题自动生成的侧边栏的最大深度

  }),
})