module.exports = {
  publicPath: '/poplar',
  pluginOptions: {
    i18n: {
      locale: 'zh',
      fallbackLocale: 'en',
      localeDir: 'locales',
      enableInSFC: true
    }
  },
  devServer: {
        host: '0.0.0.0', // 允许外部ip访问
        port: 8080, // 端口
        https: false, // 启用https
        proxy: ''
    }
}
