import React, { Component } from 'react';

export default class MakeNew extends Component {
    constructor(props) {
        super(props);
        this.frontInput = React.createRef();
        this.backInput = React.createRef();
    }
    handleClick() {
        const front = this.frontInput.current.value;
        const back = this.backInput.current.value;
        if (front.length === 0 || back.length === 0) {
            console.error('empty');
        }
        this.props.onSubmit({ front, back });
    }
    render() {
        return <div style={{
            border: '1px solid black',
            padding: '20px',
            margin: '20px',
            width: '500px',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'flex-start'
        }}>
            Front
            <input ref={this.frontInput}  style={{
                width: '100%',
                height: '10em'
            }} />
            <div style={{ height: '1em' }} />
            Back
            <input ref={this.backInput} style={{
                width: '100%',
                height: '10em'
            }} />
            <div style={{ height: '1em' }} />
            <button onClick={this.handleClick.bind(this)}>submit</button>
        </div>
    }
}
