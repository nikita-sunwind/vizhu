import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';

import 'bootstrap/dist/css/bootstrap.min.css';
import 'font-awesome/css/font-awesome.min.css';

import AppRouter from './Router';
import AppStore from './Store';

ReactDOM.render(
    <Provider store={AppStore}>
        <AppRouter />
    </Provider>,
    document.getElementById('root')
);
