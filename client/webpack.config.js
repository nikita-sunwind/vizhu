/* eslint-disable no-undef */

const webpack = require('webpack');
const CompressionPlugin = require('compression-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');


var plugins = [
    new webpack.DefinePlugin({
        'process.env': {
            NODE_ENV: JSON.stringify(process.env.NODE_ENV),
        },
    }),
];

if (process.env.NODE_ENV === 'production') {
    plugins.push(
        new webpack.optimize.OccurrenceOrderPlugin(),
        new webpack.optimize.UglifyJsPlugin(),
        new CompressionPlugin(),
        new HtmlWebpackPlugin({title: 'vizhu', hash: true, template: './src/index.ejs'})
    );
} else {
    plugins.push(
        new HtmlWebpackPlugin({title: 'vizhu (development mode)', hash: true, template: './src/index.ejs'})
    );
}

module.exports = {

    entry: './src/vizhu.js',

    output: {
        path: __dirname + '/dist',
        filename: 'bundle.js',
        publicPath: '/static/',
    },

    module: {
        rules: [
            {test: /\.(js|jsx)$/, use: ['babel-loader', 'eslint-loader']},
            {test: /\.ejs$/, use: 'ejs-loader'},
            {test: /\.css$/, use: ['style-loader', 'css-loader']},
            {test: /\.svg(\?v=\d+\.\d+\.\d+)?$/, use: 'file-loader?mimetype=image/svg+xml'},
            {test: /\.woff(\?v=\d+\.\d+\.\d+)?$/, use: 'file-loader?mimetype=application/font-woff'},
            {test: /\.woff2(\?v=\d+\.\d+\.\d+)?$/, use: 'file-loader?mimetype=application/font-woff2'},
            {test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/, use: 'file-loader?mimetype=application/octet-stream'},
            {test: /\.eot(\?v=\d+\.\d+\.\d+)?$/, use: 'file-loader?mimetype=application/vnd.ms-fontobject'},
        ],
    },

    resolve: {
        extensions: ['.jsx', '.js'],
    },

    plugins: plugins,

};
