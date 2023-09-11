odoo.define("gevi_url_access_restriction.WarningMessage", function (require) {
  "use strict";

  var core = require('web.core');
//  var AbstractAction = require('web.AbstractAction');
  var Widget = require('web.ActionManager');
  var ControlPanelMixin = require('web.ControlPanelMixin');

  var WarningMessage = ActionManager.extend(ControlPanelMixin, {
    'template': 'WarningMessageTemplate'
//    ,
//    init: function(parent, context) {
//      this._super.apply(this, arguments);
//      $(".o_control_panel").addClass('oe_hidden');
//    },
//    destroy: function () {
//      $(".o_control_panel").removeClass('oe_hidden');
//      return this._super.apply(this, arguments);
//    },
  });

  core.action_registry.add('warning_message', WarningMessage);
});
