import React from 'react';
import ReactDOM from 'react-dom';

import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';

import _ from "lodash";

import { ApplicationContainer } from '/components/business/appbase';
import {ApplicationPage} from '/common_lib';

import "./main.scss";

/*********************************************************************************
 * Purpose: Signup user
 *
 * Props
 *      current_user: current user
 *      csrf_token:   the csrf token
 *      set_alert:    a function to set alert
 */

class SignupApplicationPage extends React.Component {
    componentDidMount() {
        const alert = this.props.app_context.alert;
        if (!_.isUndefined(alert)) {
            this.props.set_alert(alert.variant, alert.message);
        }
    }

    render() {
        return (
            <Container className="signup-form-container">
                <Row>
                    <Col>
                        <h4 className="text-center pt-3 pb-3">Signup to SparkBase</h4>
                    </Col>
                </Row>
                <Form action="/ui/signup" method="POST">
                    <input
                        type="hidden"
                        name="csrfmiddlewaretoken"
                        value={this.props.csrf_token}
                    />

                    <Form.Group as={Row} controlId="firstname">
                        <Form.Label column sm={3}>First name</Form.Label>
                        <Col>
                            <Form.Control name="first_name" />
                        </Col>
                    </Form.Group>

                    <Form.Group as={Row} controlId="lastname">
                        <Form.Label column sm={3}>Last name</Form.Label>
                        <Col>
                            <Form.Control name="last_name" />
                        </Col>
                    </Form.Group>

                    <Form.Group as={Row} controlId="username">
                        <Form.Label column sm={3}>Username</Form.Label>
                        <Col>
                            <Form.Control name="username" />
                        </Col>
                    </Form.Group>

                    <Form.Group as={Row} controlId="email">
                        <Form.Label column sm={3}>Email</Form.Label>
                        <Col>
                            <Form.Control name="email" />
                        </Col>
                    </Form.Group>

                    <Form.Group as={Row} controlId="password">
                        <Form.Label column sm={3}>Password</Form.Label>
                        <Col>
                            <Form.Control type="password" name="password" />
                        </Col>
                    </Form.Group>

                    <Form.Group as={Row} controlId="password1">
                        <Form.Label column sm={3}>Password (confirm)</Form.Label>
                        <Col>
                            <Form.Control type="password" name="password1" />
                        </Col>
                    </Form.Group>

                    <div className="text-center">
                        <Button type="submit">Signup</Button>
                    </div>
                </Form>
            </Container>
        )
    }
}

$(function() {
    const page = new ApplicationPage();

    ReactDOM.render(
        <ApplicationContainer
            current_user={page.current_user}
            csrf_token={page.csrf_token}
            init_menu_key={page.init_menu_key}
            app_context={page.app_context}
        >
            <SignupApplicationPage />
        </ApplicationContainer>,
        document.getElementById('app')
    );
});
