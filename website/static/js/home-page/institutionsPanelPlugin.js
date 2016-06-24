/**
 * Display a horizontal listing of clickable OSF4I logos (links to institution landing pages).
 */
'use strict';

var $ = require('jquery');
var m = require('mithril');
var utils = require('js/components/utils');
var required = utils.required;
var lodashChunk  = require('lodash.chunk');

var institutionComps = require('js/components/institution');
var carouselComps = require('js/components/carousel');

var Institution = institutionComps.InstitutionImg;
var Carousel = carouselComps.Carousel;
var CarouselRow = carouselComps.CarouselRow;

var CAROUSEL_WIDTH = 6;
var REDUCED_CAROUSEL_WIDTH = CAROUSEL_WIDTH - 1;
var COLUMN_WIDTH = Math.floor(12 / CAROUSEL_WIDTH);

var InstitutionsPanel = {
    controller: function() {
        // Helper method to render logo link
        this.renderLogo = function(inst, opts) {
            var href = '/institutions/' + inst.id + '/';
            var columnWidth = COLUMN_WIDTH.toString();
            return m('.col-sm-' + columnWidth, {style: {'display':'inline-block', 'float':'none'}}, [
                m('a', {href: href, className: 'thumbnail', style: {'background': 'inherit', 'border': 'none'}},
                    [m.component(Institution,
                                {
                                    className: 'img-responsive',
                                    style: {'background-color': 'white'},
                                    name: inst.name,
                                    logoPath: inst.logoPath,
                                    muted: opts.muted,
                                })])
            ]);
        };
    },
    view: function(ctrl, opts) {
        var affiliated = required(opts, 'affiliatedInstitutions');
        var allInstitutions = required(opts, 'allInstitutions');

        var affiliatedIds = affiliated.map(function(inst) { return inst.id; });
        var unaffiliated = allInstitutions.filter(function(inst) {
            return $.inArray(inst.id, affiliatedIds) === -1;
        });

        var institutions = affiliated.concat(unaffiliated);
        var controls = institutions.length > CAROUSEL_WIDTH;
        if (controls && (12 % CAROUSEL_WIDTH) === 0 && CAROUSEL_WIDTH > REDUCED_CAROUSEL_WIDTH) {
            CAROUSEL_WIDTH = REDUCED_CAROUSEL_WIDTH;
        }

        var groupedInstitutions = lodashChunk(institutions, CAROUSEL_WIDTH);
        return m.component(Carousel, {controls: controls},
            groupedInstitutions.map(function(instGroup, idx) {
                var active = idx === 0;
                return m.component(CarouselRow, {active: active}, instGroup.map(function(inst) {return ctrl.renderLogo(inst, {}); }));
            })
        );
    }
};

module.exports = InstitutionsPanel;
