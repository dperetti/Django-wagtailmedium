module.exports = {
  entry: '/src/wagtailmedium/main.js', // this is our main input
  output: {
    path: '/project/wagtailmedium/static/wagtailmedium',
    filename: 'wagtailmedium.js', // this our output
    publicPath: '/static/wagtailmedium/',
  },
  module: {
    loaders: [
      // compile imported javascript files using babel
      {
        test: /\.js$/,
        exclude: /node_modules/,
        loader: 'babel-loader',
        query: {
          presets: ['react', 'es2015', 'stage-0'],
        },
      },
      // compile and bundle imported less & css
      {
        test: /(.less|.css)$/,
       // exclude: /bootstrap\/fonts/,
        loader: 'style!css!less',
      },
      // bundle imported fonts
      {
        test: /\.(ttf|eot|svg|woff|woff2)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
        loader: 'file-loader',
      },
    ],
  },
}
