import React from 'react';
import ReactDOM from 'react-dom';
import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Table from 'react-bootstrap/Table';

import _ from 'lodash';

import { ApplicationContainer } from '/components/business/appbase';

import {ApplicationPage} from '/common_lib';

import {TestDialogBox} from '/components/generic/dialogbox/test_main.jsx';

import "./test.scss";


/*********************************************************************************
 * Purpose: Page to view an application
 *
 * Props
 *      current_user: current user
 *      csrf_token:   the csrf token
 *      set_alert:    a function to set alert
 */

class TestApplicationPage extends React.Component {
    testClasses = [
        {
            category    : "generic",
            component   : "dialogbox",
            classname   : "DialogBox",
            create      : () => <TestDialogBox />,
            tested: "2021-11-25"
        }
    ];

    renderTestClass() {
        const testClass = _.find(
            this.testClasses,
            testClass => testClass.classname === this.props.classname
        );
        return testClass.create();
    }

    renderTableRow(idx) {
        const testClass = this.testClasses[idx];
        const componentGroupCouont = this.testClasses.filter(x => x.component === testClass.component).length;

        if ((idx === 0) || (idx > 0 && this.testClasses[idx-1].component !== testClass.component)) {
            return (
                <tr key={testClass.classname}>
                    <td rowSpan={componentGroupCouont}>{testClass.category}</td>
                    <td rowSpan={componentGroupCouont}>{testClass.component}</td>
                    <td>
                        <a href={`?classname=${testClass.classname}`} target="_blank">
                            {testClass.classname}
                        </a>
                    </td>
                    <td>{testClass.tested}</td>
                </tr>
            );
        } else {
            return (
                <tr key={testClass.classname}>
                    <td>
                        <a href={`?classname=${testClass.classname}`} target="_blank">
                            {testClass.classname}
                        </a>
                    </td>
                    <td>{testClass.tested}</td>
                </tr>
            );
        }
        return ret;
    }


    renderTestList() {
        return <>
            <Row>
                <Col>
                    <h1>Main Test Page</h1>
                    <Table hover size="sm" className="test-table">
                        <thead className="thead-dark">
                            <tr>
                                <th data-role='category'>Category</th>
                                <th data-role='component'>Component</th>
                                <th data-role='class'>Class</th>
                                <th data-role='tested'>Tested</th>
                            </tr>
                        </thead>
                        <tbody>
                            {
                                this.testClasses.map((testClass, idx) => this.renderTableRow(idx))
                            }
                        </tbody>
                    </Table>
                </Col>
            </Row>
        </>;
    }
    render() {
        if (this.props.classname) {
            return (
                <Container fluid>
                    {
                        this.renderTestClass()
                    }
                    <br/><br/><br/><br/>
                    <p>
                        <a href="/ui/test">Go back</a>
                    </p>
                </Container>                
            );
        } else {
            return this.renderTestList();
        }
        
    }
}

$(function() {
    const page = new ApplicationPage();
    const classname = new URLSearchParams(globalThis.location.search).get('classname');

    ReactDOM.render(
        <ApplicationContainer
            current_user={page.current_user}
            csrf_token={page.csrf_token}
            init_menu_key={page.init_menu_key}
            app_context={page.app_context}
            classname={classname}
        >
            <TestApplicationPage />
        </ApplicationContainer>,
        document.getElementById('app')
    );
});
