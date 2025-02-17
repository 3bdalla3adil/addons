/** @odoo-module */

import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, useState} from "@odoo/owl";

export class BeautifulController extends Component {
    setup() {
        this.orm = useService("orm");

        // The controller create the model and make it reactive so whenever this.model is
        // accessed and edited then it'll cause a rerendering
        this.model = useState(
            new this.props.Model(
                this.orm,
                this.props.resModel,
                this.props.fields,
                this.props.archInfo,
                this.props.domain
            )
        );

        onWillStart(async () => {
            await this.model.load();
        });
    }
}

BeautifulController.template = "beauty_clinic_management.View";
BeautifulController.components = { Layout };