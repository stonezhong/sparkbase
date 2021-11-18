import React from 'react';
import ReactDOM from 'react-dom';

import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';

import { ApplicationContainer } from '/components/business/appbase';

import {ApplicationPage} from '/common_lib';

/*********************************************************************************
 * Purpose: Page to view an application
 *
 * Props
 *      current_user: current user
 *      csrf_token:   the csrf token
 *      set_alert:    a function to set alert
 *      app_context:  application context
 */

class ErrorApplicationPage extends React.Component {
    render() {
        return (
            <>
                <Row>
                    <Col>
                        <h1>{this.props.app_context.subject}</h1>
                        <hr />
                        <p>{this.props.app_context.message}</p>
                    </Col>
                </Row>
            </>
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
            <ErrorApplicationPage />
        </ApplicationContainer>,
        document.getElementById('app')
    );
});
