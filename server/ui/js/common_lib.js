import $ from "jquery";
import _ from "lodash";

export async function setStateAsync(component, state) {
    return new Promise((resolve) => component.setState(state, resolve));
}

export class ApplicationPage {
    constructor() {
        this.current_user       = this.get_meta_json("user");
        this.app_context        = this.get_meta_json("app_context", {});
        this.csrf_token         = this.get_meta("csrf");
        this.init_menu_key      = this.get_meta("init_menu_key");
    }

    get_meta_json(name, default_value=null) {
        const elements = $(`meta[name='${name}']`);
        if (elements.length > 0)
            return JSON.parse(elements[0].content);
        else
            return default_value
    }

    get_meta(name) {
        const elements = $(`meta[name='${name}']`);
        if (elements.length > 0)
            return elements[0].content;
        else
            return "";
    }
}

export function bless_modal(modal_id) {
    const modal_content = $(`[data-modal-id=${modal_id}] > .modal-content`);
 
    modal_content.resizable({});
    modal_content.draggable({
        handle: ".modal-header",
    });
    modal_content.position({
        of: $(window)
    });
}
