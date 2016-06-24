
//TODO uncomment and write more tests
/* Tests for myprojects.js for My Projects in Dashboard */
/*global describe, it, expect, example, before, after, beforeEach, afterEach, mocha, sinon*/
'use strict';
var assert = require('chai').assert;

var $ = require('jquery');
var $osf = require('js/osfHelpers');
var fb = require('js/myProjects.js');
var m = require('mithril');

var LinkObject = fb.LinkObject;

describe('fileBrowser', function() {
    describe('LinkObject', function () {
        var collection;
        var tag;
        var name;
        var node;

        before(function () {
            collection = new LinkObject('collection', {
                path: 'users/me/nodes/',
                query: {'related_counts': 'children'},
                systemCollection: true
            }, 'All My Projects');
            tag = new LinkObject('tag', { tag : 'something', query : { 'related_counts' : true }}, 'Something Else');
            name = new LinkObject('name', { id : '8q36f', query : { 'related_counts' : true }}, 'Caner Uguz');
            node = new LinkObject('node', { id : 'qwerty'}, 'Node Title');
        });

        describe('#attributes', function () {
            it('should return an id of 1', function () {
                assert.equal(collection.id, 1);
            });
            it('should throw error when no arguments passed', function () {
                assert.throws(function(){ var missing = new LinkObject(); }, Error);
            });
        });
    });
});