import React, { Component } from 'react';

export default class Main extends Component {

    static propTypes = {
        children: React.PropTypes.node
    }

    render() {
        return (
            <div>
                {this.props.children}
            </div>
        );
    }

}
