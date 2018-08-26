import React, { Component } from 'react';

export default class Option extends Component {
    handleClick() {
        this.props.onClick(this.props.ease);
    }
    render() {
        return <div style={{
            display: "inline-flex",
            flexDirection: "column",
        }}>
        <div style={{
            fontSize: '0.6em'
        }}>
        {this.props.top}
        </div>
        <button onClick={this.props.onClick} style={{
            width: '6em',
            marginLeft: '0.15em',
            marginRight: '0.15em',
        }}>{this.props.front}</button>
        </div>
    }
}
