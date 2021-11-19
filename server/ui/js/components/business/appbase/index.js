import React from 'react';

import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Container from 'react-bootstrap/Container';
import DropdownButton from 'react-bootstrap/DropdownButton'
import Dropdown from 'react-bootstrap/Dropdown'
import Alert from 'react-bootstrap/Alert';

import { v4 as uuidv4 } from 'uuid';
import { setStateAsync } from '/common_lib';

import "./main.scss";

/*********************************************************************************
 * Purpose: Page to view an application
 *
 * Props
 *      current_user: current user  
 *      init_menu_key: the default activate key
 *      
 *  It will inject all it's property to it's children
 *  It will also pass a property set_alert(variant, text) method to it's children so they can report error
 */
class GlobalHeader extends React.Component {
    render() {
        return <Navbar fixed="top" expand="sm" variant="dark" className="global-header">
            <Navbar.Brand href="#">
                <img
                    src="/static/images/logo.png"
                    alt="Logo"
                    className="d-inline-block align-top"
                />
                <span className="font-weight-bold">
                    SparkBase
                </span>
            </Navbar.Brand>
            <Nav variant="pills" className="mr-auto" defaultActiveKey={this.props.init_menu_key}>
                { 
                    !this.props.current_user.is_authenticated && 
                    <Nav.Link 
                        eventKey="login" 
                        href="/ui/login"
                    >Login</Nav.Link>
                }
                {/* { 
                    !this.props.current_user.is_authenticated && 
                    <Nav.Link 
                        eventKey="signup" 
                        href="/ui/signup"
                    >Signup</Nav.Link>
                } */}
            </Nav>
            {
                this.props.current_user.is_authenticated &&
                <DropdownButton 
                    id="user-profile" 
                    title={this.props.current_user.username} 
                    menuAlign="right"
                    variant="light"
                >
                    <Dropdown.Item href="/accounts/logout">Logout</Dropdown.Item>
                </DropdownButton>
            }
        </Navbar>;
    }
}

/*********************************************************************************
 * Purpose: Page to view an application
 *
 * Props
 *      current_user: current user  
 *      
 *  It will inject all it's property to it's children
 *  It will also pass a property set_alert(variant, text) method to it's children so they can report error
 */
export class ApplicationContainer extends React.Component {
    state = {
        error_msgs: {}
    }

    set_alert = async (variant, text) => {
        const key = uuidv4();
        await setStateAsync(this, state=> {
            state.error_msgs[key] = {
                variant: variant,
                text: text
            }
            return state;
        });
    }

    render() {
        const props = {... this.props, set_alert: this.set_alert};
        return <>
            <GlobalHeader {... this.props} />
            <Container fluid className="app-container">
                {
                    (Object.keys(this.state.error_msgs).length > 0) && <Row>
                        <Col>
                        {
                            Object.entries(this.state.error_msgs).map(
                                (entry) => <Alert
                                    key={entry[0]}
                                    variant={entry[1].variant}
                                    onClose={() => {
                                        setStateAsync(this, state => {
                                            delete this.state.error_msgs[entry[0]];
                                            return state
                                        })
                                    }}
                                    dismissible
                                >
                                    {entry[1].text}
                                </Alert>
                            )
                        }
                        </Col>
                    </Row>
                }
                {
                    React.Children.map(
                        this.props.children, 
                        child => React.cloneElement(child, props, null)
                    )
                }
            </Container>
        </>;
    }
}
