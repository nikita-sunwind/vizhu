import React, { Component } from 'react';
import { Router, Route, browserHistory } from 'react-router';

import { Main } from './containers';

export default class AppRouter extends Component {

    render() {
        return (
            <Router history={browserHistory}>
                <Route path='/' component={Main}>
                </Route>
            </Router>
        );
    }

}
