/** @odoo-module **/

import { Component, onMounted, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";


export class StatsView extends Component {

    static template = "cancer_center.StatsView";

    setup() {
        // useState is required for reactivity
        this.rpc = useService("rpc");
        this.state = useState({
            cure_statistics: [],
            today_cures: []
        });

        // use OWL lifecycle hook
        onMounted(this.loadCureStatistics);
        onMounted(this.loadTodayCures);
    }

    loadCureStatistics = async () => {
        const result = await this.rpc("/web/dataset/call_kw", {
                                model: "cancer_center.cure.statistics",
                                method: "search_read",
                                kwargs: {},
                                args: [],
                                });
            this.state.cure_statistics = result;
    }
    
    loadTodayCures = async () => {
        const today = luxon.DateTime.now().toISODate();
        const result = await this.rpc("/web/dataset/call_kw", {
                                model: "cancer_center.cure",
                                method: "search_read",
                                args: [[["date_of_cure", "=", today]]],
                                kwargs: {
                                    fields: [
                                            "patient_id",
                                            "medication_id",
                                            "height", 
                                            "weight", 
                                            "calculated_dose",
                                            "status_label",
                                            "reaction_ids"
                                        ],
                                    order: "create_date desc",
                                },
                                });
            console.log(result)
            this.state.today_cures = result;
    }


    openCureListView() {
    const today = luxon.DateTime.now().toISODate();
    this.env.services.action.doAction({
        type: 'ir.actions.act_window',
        name: 'Cures',
        res_model: 'cancer_center.cure',
        view_mode: 'tree,form',
        views: [
            [this.env.ref('cancer_center.cancer_center_patient_cure_view_tree').id, 'tree'],
            [false, 'form']
        ], // will use default view unless you specify ID
        target: 'current',
        domain: [['date_of_cure', '=', today]],
    });
    }
}

registry.category("actions").add("cancer_center.action_stats_view", StatsView)