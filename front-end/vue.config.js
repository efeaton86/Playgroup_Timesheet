const BundleTracker = require("webpack-bundle-tracker");

const pages = {
  'timesheetVueCalendar': {
    entry: './src/apps/timesheet/timesheetVueCalendar.js',
    chunks: ['chunk-vendors']
  },
  'timesheetTimeEntryApproval': {
    entry: './src/apps/timesheet/timesheetTimeEntryApproval.js',
    chunks: ['chunk-vendors']
  },
  'timesheetEntryForm': {
    entry: './src/apps/timesheet/timesheetEntryForm.js',
    chunks: ['chunk-vendors']
  },
}

module.exports = {
  pages: pages,
  filenameHashing: false,
  productionSourceMap: false,

  publicPath: process.env.NODE_ENV === 'production'
    ? ''
    : 'http://localhost:8080/',

  outputDir: '../static/vue/',

  chainWebpack: config => {
    config.optimization
      .splitChunks({
        cacheGroups: {
          vendor: {
            test: /[\\/]node_modules[\\/]/,
            name: "chunk-vendors",
            chunks: 'all',
            priority: 1
          }
        }
      })

    Object.keys(pages).forEach(page => {
      config.plugins.delete(`html-${page}`)
      config.plugins.delete(`preload-${page}`)
      config.plugins.delete(`prefetch-${page}`)
    })

    config
      .plugin('BundleTracker')
      .use(BundleTracker, [{ filename: '../front-end/webpack-stats.json' }])

    config.resolve.alias
      .set('__STATIC__', 'static')

    config.devServer
      .public('http://localhost:8080')
      .host('localhost')
      .port(8080)
      .hotOnly(true)
      .watchOptions({ poll: 1000 })
      .https(false)
      .headers({ 'Access-Control-Allow-Origin': ['*'] })
  },

  lintOnSave: false
}
