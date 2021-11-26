const webpack = require("webpack");
const path = require("path");

module.exports = (env, argv) => {
    // command line arguments passed to argv
    // argv.mode: 'development' or 'production'

    const devtool = argv.mode=="production"?undefined:'inline-source-map';

    return {
        mode: argv.mode,
        externals: {
            jquery: 'jQuery',
            react: 'React',
            'react-dom': 'ReactDOM',
            'react-bootstrap/Button':           ['ReactBootstrap', 'Button'],
            'react-bootstrap/Col':              ['ReactBootstrap', 'Col'],
            'react-bootstrap/Row':              ['ReactBootstrap', 'Row'],
            'react-bootstrap/Form':             ['ReactBootstrap', 'Form'],
            'react-bootstrap/Container':        ['ReactBootstrap', 'Container'],
            'react-bootstrap/Modal':            ['ReactBootstrap', 'Modal'],
            'react-bootstrap/Table':            ['ReactBootstrap', 'Table'],
            'react-bootstrap/Spinner':          ['ReactBootstrap', 'Spinner'],
            'react-bootstrap/Alert':            ['ReactBootstrap', 'Alert'],
            'react-bootstrap/Navbar':           ['ReactBootstrap', 'Navbar'],
            'react-bootstrap/Nav':              ['ReactBootstrap', 'Nav'],
            'react-bootstrap/DropdownButton':   ['ReactBootstrap', 'DropdownButton'],
            'react-bootstrap/Dropdown':         ['ReactBootstrap', 'Dropdown'],
            'lodash': '_',
            '@ckeditor/ckeditor5-build-classic': 'ClassicEditor',
            '@ckeditor/ckeditor5-react': 'CKEditor',
        },
        resolve: {
            extensions: ['.js', '.jsx'],
            roots: [
                path.resolve('./ui/js'),
            ],
        },
        entry: {
            "test"              : '/pages/test/main.jsx',
            "home"              : '/pages/home/main.jsx',
            "login"             : '/pages/login/main.jsx',
            "signup"            : '/pages/signup/main.jsx',
            "error"             : '/pages/error/main.jsx',
        },
        output: {
            path: path.resolve("ui", "static", "js-bundle"),
            filename: "[name].js"
        },
        module: {
            rules: [
                {
                    test: /\.(js|jsx)$/,
                    exclude: /node_modules/,
                    use: [
                        {
                            loader: "babel-loader",
                        }
                    ],
                },
                {
                    test: /\.s[ac]ss$/,
                    use: [
                        'style-loader',
                        'css-loader',
                        'sass-loader',
                    ]
                }
            ]
        },
        devtool
    }
};
