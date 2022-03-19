/*
 * View model for LCD1602
 */
$(function () {
    function LCD1602ViewModel(parameters) {
        var PLUGIN_ID = "LCD1602";

        var self = this;

        self.settingsViewModel = parameters[0];
    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: LCD1602ViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        dependencies: ["settingsViewModel"],
        elements: [
            document.getElementById("settings_LCD1602")
        ]
    });
});