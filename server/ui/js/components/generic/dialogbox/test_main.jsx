import React from 'react';
import Form from 'react-bootstrap/Form';

import {DlgBoxAgent, DialogBoxStackProvider} from './index.jsx';
import Button from 'react-bootstrap/Button';

import _ from "lodash";

/*********************************************************************************
 * Purpose: Test for dialogbox component
 *
 * Props
 */

class Agent1 extends DlgBoxAgent {
    // constructor(dbsRef) {
    //     super(dbsRef);
    // }

    getInitSubState() {
        return {
            price: "10.0"
        }
    }

    onSubStateUpdated(dlgbox, state, newSubState) {
        const price = Number(newSubState.price);
        if (_.isNaN(price)) {
            dlgbox.action_set(state, "help", action => {
                return {
                    text: "Help",
                    allowed: true
                }
            });
            dlgbox.title_set(state, "Price is invalid")
        } else {
            // remove Help button when price is valid number
            dlgbox.action_remove(state, "help");
            dlgbox.title_set(state, "DialogBox with agent")
        }
    }

    renderContent(dlgbox) {
        const subState = dlgbox.state.subState;
        return (
            <Form.Group controlId="price">
            <Form.Label>Price</Form.Label>
            <Form.Control 
                value={subState.price}
                onChange={(evt) => {
                    dlgbox.updateSubStateField("price", evt.target.value)
                }}
            />
        </Form.Group>

        );
    }

    async onAction(dlgbox, name) {
        if (name === 'help') {
            this.openDialog({
                title: "Help Contents",
                size: "sm",
                content: <p>Blah...</p>
            });
        }
    }
}

export class TestDialogBox extends React.Component {
    render() {
        return (
            <DialogBoxStackProvider.Consumer>
                {
                    (dbsRef) => <>
                        <h1>Test Dialogbox</h1>
                        <Button
                            onClick={(evt) => {
                                dbsRef.current.openDialog({
                                    title: "Simple dialogbox",
                                    size: "md",
                                    content: <p>Hello</p>
                                });
        
                            }}
                            size="sm"
                        >
                            Open simple dialog
                        </Button>
                        <Button
                            onClick={(evt) => {
                                dbsRef.current.openDialog({
                                    title: "DialogBox with agent",
                                    size: "md",
                                    agent: new Agent1(dbsRef)
                                });
        
                            }}
                            size="sm"
                            className="ms-2"
                        >
                            Open dialogbox with agent
                        </Button>
                    </>                
                }
            </DialogBoxStackProvider.Consumer>
        );
    }
}
