'use strict';

var ko = require('knockout');
var $ = require('jquery');
var Raven = require('raven-js');
var koHelpers = require('js/koHelpers');
var $osf = require('js/osfHelpers');

var MESSAGE_TIMEOUT = 5000;

var DEFAULT_FORWARD_BOOL = true;

/**
 * Knockout view model for the Forward node settings widget.
 */
var ViewModel = function(url, nodeId) {

    var self = this;

    // Forward configuration
    self.url = ko.observable().extend({
        ensureHttp: true,
        url: true,
        required: true
    });
    ko.validation.addAnonymousRule(
        self.url,
        koHelpers.makeRegexValidator(
            new RegExp(nodeId, 'i'),
            'Components cannot link to themselves',
            false
        )
    );
    self.label = koHelpers.sanitizedObservable();

    // Flashed messages
    self.message = ko.observable('');
    self.messageClass = ko.observable('text-info');

    self.validators = ko.validatedObservable({
        url: self.url,
    });


    /**
     * Update the view model from data returned from the server.
     */
    self.updateFromData = function(data) {
        self.url(data.url);
        self.label(data.label);
    };

    self.fetchFromServer = function() {
        $.ajax({
            type: 'GET',
            url: url,
            dataType: 'json'
        }).done(function(response) {
            self.updateFromData(response);
        }).fail(function(xhr, textStatus, error) {
            self.changeMessage('Could not retrieve Forward settings at ' +
                'this time. Please refresh ' +
                'the page. If the problem persists, email ' +
                '<a href="mailto:support@osf.io">support@osf.io</a>.',
                'text-danger');
            Raven.captureMessage('Could not GET get Forward addon settings.', {
                url: url,
                textStatus: textStatus,
                error: error
            });
        });
    };

    // Initial fetch from server
    self.fetchFromServer();

    function onSubmitSuccess() {
        self.changeMessage(
            'Successfully linked to <a href="' + self.url() + '">' + self.url() + '</a>.',
            'text-success',
            MESSAGE_TIMEOUT
        );
    }

    function onSubmitError(xhr, status) {
        self.changeMessage(
            'Could not change settings. Please try again later.',
            'text-danger'
        );
    }

    /**
     * Submit new settings.
     */
    self.submitSettings = function() {
        $osf.putJSON(
            url,
            ko.toJS(self)
        ).done(
            onSubmitSuccess
        ).fail(
            onSubmitError
        );
    };

    /** Change the flashed message. */
    self.changeMessage = function(text, css, timeout) {
        self.message(text);
        var cssClass = css || 'text-info';
        self.messageClass(cssClass);
        if (timeout) {
            // Reset message after timeout period
            setTimeout(function() {
                self.message('');
                self.messageClass('text-info');
            }, timeout);
        }
    };

};

// Public API
function ForwardConfig(selector, url, nodeId) {
    var self = this;
    self.viewModel = new ViewModel(url, nodeId);
    $osf.applyBindings(self.viewModel, selector);
}

module.exports = ForwardConfig;

