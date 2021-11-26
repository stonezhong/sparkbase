import React from 'react';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Modal from 'react-bootstrap/Modal';
import { v4 as uuidv4 } from 'uuid';
import _ from 'lodash';
import {bless_modal, setStateAsync} from '/common_lib';
import {DialogBoxStackProvider} from '/components/generic/dialogbox/providers.jsx';

export {DialogBoxStackProvider};

import "./main.scss";

/*********************************************
 * You need to derive from DlgBoxAgent in case you want to create
 * an interactive dialbogbox
 * - Constructor
 *       You can extend it, will receive dbsRef, which is a 
 *       reference to dialog box stack reference. So you can use it to launch 
 *       new dialogbox
 * 
 * - getInitSubState
 *       diabogbox component has a subState field inside it's state to store
 *       custom state. An agent can return initial subState in this function
 * 
 * - openDialog
 *       Use the same dialog box stack reference to launch a new dialogbox on
 *       the top.
 * 
 * - onSubStateUpdated
 *       called when subState is about to be updated. Usually is triggered
 *       by someone calls DialogBox.updateSubState.
 *       return value is not looked at. But you can call functions like
 *       action_remove/action_set/set_title to add, remove, update action buttons
 *       or update dialog title.
 * 
 *  - renderContent(dlgbox)
 *       You need to impmement this function to return component that will be
 *       rendered at the client area of the dialogbox.
 *
 *  - onAction(dlgbox, name)       
 *       Called when user want to perform an action.
 */
export class DlgBoxAgent {
    /*********************************************************************************
     * dbsRef: ref to DialogBoxStack
     */
    constructor(dbsRef) {
        this.dbsRef = dbsRef;
    }

    async getInitSubState(dlgbox) {
        return {};
    }

    // this is a async function since inner calls async function
    openDialog(options) {
        return this.dbsRef.current.openDialog(options);
    }

    //-----------------------------------------------------------------
    // when updating state, you should use state specified here
    // instead of dlgbox.state
    //-----------------------------------------------------------------
    onSubStateUpdated(dlgbox, state, newSubState) {
    }

    renderContent(dlgbox) {
        return null;
    }

    async onAction(dlgbox, name) {

    }
}

/*********************************************************************************
 * Purpose: A dialogbox wrapper
 * 
 * - Pass an agent if you want a dynamic dialog box
 * 
 * - action_remove
 *       remove an action.
 * 
 * - action_set
 *       define a new action or overwrite an existing action
 * 
 * - title_set
 *       Set dialogbox title
 * 
 * - updateSubState
 *       Update subState, will trigger agent's onSubStateUpdated
 *
 * - updateSubStateField
 *       Update a field in subState, will trigger agent's onSubStateUpdated
 * 
 * - close
 *       Close the dialogbox, reset status
 * 
 * - onAction
 *       Dispatch action to agent. And handle close action as well.
 * 
 * - openDialog
 *       Opens a dialogbox, user should not call this function directly.
 * 
 * - render
 *       for react
 */

export class DialogBox extends React.Component {
    state = {
        show:       false,
        title:      '',
        size:       'sm',
        actions:    {},
        agent:      null,
        onClose:    null,  // a callback to notify the stack the dialogbox is closed
        subState:   {},
    };

    modal_id = uuidv4();

    // Following functions are only called in onSubStateUpdated from agent
    action_remove = (state, name) => {
        if (name in state.actions) {
            delete state.actions[name];
        }
    }
    action_set = (state, name, cb) => {
        const action = state.actions[name] || null;
        const {text, allowed} = cb(action);
        state.actions[name] = {text, allowed};
    }
    title_set = (state, title) => {
        state.title = title;
    }

    // Update substate, the update(state.subState) will return new subState
    updateSubState = async (update) => {
        await setStateAsync(this, state => {
            const newSubState = update(state.subState);
            state.subState = newSubState;

            if (this.state.agent) {
                this.state.agent.onSubStateUpdated(this, state, newSubState);
            }

            return state;
        });
    }

    // Update a subState field
    updateSubStateField = async (fieldName, fieldValue) => {
        await setStateAsync(this, state => {
            state.subState[fieldName] = fieldValue;
            if (this.state.agent) {
                this.state.agent.onSubStateUpdated(this, state, state.subState);
            }

            return state;
        });
    }

    // close the dialogbox
    close = async () => {
        const onClose = this.state.onClose;
        await setStateAsync(this, {
            show: false,
            title: '',
            size: 'sm',
            actions: {},
            agent: null,
            onClose: null,
            subState: {},
        });

        await onClose();
    }

    onAction = async (name) => {
        if (!_.isNull(this.state.agent)) {
            await this.state.agent.onAction(this, name);
        }
        if (name === "close") {
            await this.close();
        }
    }

    // title            : string, the title of the dialog
    // size             : string, sm, md or lg, specify the size of the dialogbox
    // agent            : an object of class DlgBoxAgent
    // onClose          : a callback from stack, so stack can do cleanup when the dialogbox is closed
    // content          : static content, only useful when agent is null
    openDialog = async (options = {}) => {
        const {title, size, agent, onClose, content} = {
            title: '', 
            size: 'sm', 
            agent: null, 
            content: null,
            ...options
        };
        // simple case, no agent
        if (_.isNull(agent)) {
            await setStateAsync(this, {
                show: true,
                title: title,
                size: size,
                actions: {},
                agent: null,
                onClose: onClose,
                subState: {},
                content: content,
            });
            bless_modal(this.modal_id);
            return;
        }

        const subState = await agent.getInitSubState(this);
        await setStateAsync(this, state => {
            const newState = {
                show: true,
                title: title,
                size: size,
                actions: {},
                agent: agent,
                onClose: onClose,
                subState: _.clone(subState),
            };
            agent.onSubStateUpdated(this, newState, subState);
            return newState;
        });
        bless_modal(this.modal_id);
        return;
    };



    render() {
        const dlg_props = {};

        let dialogClassName = "standard-modal"
        if (this.state.size === 'sm') {
            dialogClassName += ' sm-modal'
        } else if (this.state.size === 'md') {
            dialogClassName += ' md-modal'
        } else if (this.state.size === 'lg') {
            dialogClassName += ' lg-modal'
        }
        if ('dialogClassName' in this.props) {
            dialogClassName += (' ' + this.props.dialogClassName);
        }

        return (
            <Modal
                show={this.state.show}
                onHide={() => this.onAction("close")}
                backdrop="static"
                scrollable
                animation={false}
                dialogClassName={dialogClassName}
                data-modal-id={this.modal_id}
                { ... dlg_props}
            >
                <Modal.Header closeButton>
                    <Modal.Title>{this.state.show && this.state.title}</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    {
                        this.state.show && <Container fluid className="pb-2 mb-2">
                            {_.isNull(this.state.agent) && this.state.content}
                            {!_.isNull(this.state.agent) && this.state.agent.renderContent(this)}
                        </Container>
                    }
                </Modal.Body>

                <Modal.Footer>
                    {
                        this.state.show && Object.entries(this.state.actions).map(
                            (entry) => 
                                (entry[0] !== 'close') && <Button
                                    variant="primary"
                                    size="sm"
                                    key={entry[0]}
                                    onClick={(evt) => this.onAction(entry[0])}
                                    disabled={!entry[1].allowed}
                                >
                                    {entry[1].text}
                                </Button>
                        )
                    }
                    <Button 
                        variant="secondary" 
                        size="sm" 
                        onClick={(evt) => this.onAction("close")}
                    >
                        Close
                    </Button>
                </Modal.Footer>
            </Modal>
        );
    }
}

export class DialogBoxStack extends React.Component {
    current = -1
    
    dlgBoxRefs = _.range(20).map(i => React.createRef())

    render() {
        return (<>
            {
                this.dlgBoxRefs.map((ref, idx) => <DialogBox key={idx} ref={ref}/>)
            }
        </>);
    }

    openDialog = async (options={}) => {
        const optionsEx = {...options};
        optionsEx.onClose = () => {
            this.current -= 1;
        };

        if ((this.current+1) >= this.dlgBoxRefs.length) {
            throw new Error("Too many dialogs!");
        }

        this.current += 1;

        return this.dlgBoxRefs[this.current].current.openDialog(optionsEx);
    }

}
