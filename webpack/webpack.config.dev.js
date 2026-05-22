const ESLintPlugin = require('eslint-webpack-plugin');
const Path = require('path');
const Webpack = require('webpack');
const { merge } = require('webpack-merge');
const StylelintPlugin = require('stylelint-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

const common = require('./webpack.common.js');

module.exports = merge(common, {
  mode: 'development',
  devtool: 'inline-cheap-source-map',
  output: {
    chunkFilename: 'js/[name].chunk.js',
  },
  devServer: {
    hot: true,
  },
  plugins: [
    new Webpack.DefinePlugin({
      'process.env.NODE_ENV': JSON.stringify('development'),
    }),
    new StylelintPlugin({
      files: Path.join('frontend/src', '**/*.s?(a|c)ss'),
      configFile: Path.resolve(__dirname, '../.stylelintrc.json')
    }),
    new MiniCssExtractPlugin({filename: 'css/app.css',}),
    new ESLintPlugin({
      extensions: ['js', 'jsx', 'mjs'], // 2. Add this to your plugins array
      configType: 'eslintrc',
      overrideConfigFile: Path.resolve(__dirname, '../.eslintrc'),
    }),
  ],
 module: {
    rules: [
      {
        test: /\.html$/i,
        loader: 'html-loader',
      },
      {
        test: /\.m?js$/,
        // 2. CHANGE: Exclude node_modules here too to catch all JS files
        exclude: /node_modules/,
        type: 'javascript/auto',
        use: {
          loader: 'babel-loader'
        }
      },
      {
        test: /\.s?css$/i,
        use: [
          MiniCssExtractPlugin.loader, 
          {
            loader:'css-loader',
            options: {
              sourceMap: true,
            },
          }, 
          'postcss-loader', 
          'sass-loader'
        ],
      },
    ],
  },
});
