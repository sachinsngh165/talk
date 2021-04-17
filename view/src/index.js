import React from 'react';
import ReactDOM from 'react-dom';
import { Container, Form, Divider } from 'semantic-ui-react'
import 'semantic-ui-css/semantic.min.css'
// import './adapter.js'
import {joinRoom} from './main.js'
import './index.css'

function Header(props) {
    return (
        <Container>
            <Form>
                <Form.Group unstackable widths="equal">
                    <Form.Input fluid label="Room ID" placeholder = "My Room" id="roomId"/>
                    <Form.Input fluid label="Enter Password" placeholder = "Password" type="password" id="password"/>
                </Form.Group>
                <Form.Button label="" id="join" type="submit" onClick={() => joinRoom()}>Join</Form.Button>
            </Form>
        </Container>
    );
}

class Video extends React.Component {
    render() {
        return (
            <Container>
                <Header/>
                <Divider/>
                <Container className="container">
                    <p id="response"></p>
                    <div className="video-container">
                        <video id="remote" autoPlay></video>
                        <video id="local" autoPlay muted></video>
                    </div>
                </Container>
                <footer>
                    <span id="status" className="small"></span>
            	      <p><a href="https://github.com/sachinsngh165/talk.git">Source Code</a></p>
                </footer>   
            </Container>
        );
    }
}


ReactDOM.render(
    <Video />,
    document.getElementById('root')
);
