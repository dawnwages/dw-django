const path = require('path');
const ESLintPlugin = require('eslint-webpack-plugin');

module.exports = {
  mode: 'development',
  entry: './frontend/src/scripts/index.js', 
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'dist'),
  },
  plugins: [new ESLintPlugin(options)],
  devServer: {
    static: './dist',
    hot: true,
  },
  module: {
    rules: [
        {
      test: /\.m?js$/,
      exclude: /node_modules/,
      use: {
        loader: 'babel-loader',
        options: {
            // Forces Babel to automatically detect if a file is an ES module
            sourceType: 'unambiguous', 
            presets: ['@babel/preset-env']
                }
            }
        },
        {
        test: /\.js$/,
        exclude: /node_modules/,
        resolve: {
          fullySpecified: false, // Prevents strictly requiring extensions
        },
        parser: {
          sourceType: 'module',
        },
      },
      // Add loaders here later (e.g., for CSS or Babel)
        {
        test: /\.s[ac]ss$/i,
        use: [
            'style-loader', // 3. Injects styles into DOM
            'css-loader',   // 2. Turns CSS into CommonJS
            'sass-loader',  // 1. Compiles Sass to CSS (Reads right-to-left)
        ],
        },
    ],
  },
};