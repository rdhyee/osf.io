<%inherit file="project/project_base.mako"/>
<%def name="title()">${node['title']} Registrations</%def>
<div id="registrationsListScope">
<ul id="registrationsTabs" class="nav nav-tabs" role="tablist">
  <li role="presentation" class="active">
    <a id="registrationsControl" aria-controls="registrations" href="#registrations">Registrations</a>
  </li>
  % if 'admin' in user['permissions'] and node['has_draft_registrations']:
  <li role="presentation" data-bind="visible: hasDrafts">
      <a id="draftsControl" aria-controls="drafts" href="#drafts">Draft Registrations</a>
  </li>
  % endif
</ul>
<div class="tab-content registrations-view">
  <div role="tabpanel" class="tab-pane active" id="registrations">
    <div class="row" style="min-height: 150px; padding-top:20px;">
      <div class="col-md-9">
        % if node["registration_count"]:
        <div mod-meta='{
            "tpl": "util/render_nodes.mako",
            "uri": "${node["api_url"]}get_registrations/",
            "replace": true,
            "kwargs": {"sortable": false, "pluralized_node_type": "registrations"}
            }'></div>
    ## Uncomment to disable registering Components
    ##% elif node['node_type'] != 'project':
    ##      %if user['is_admin_parent']:
    ##          To register this component, you must <a href="${parent_node['url']}registrations"><b>register its parent project</b></a> (<a href="${parent_node['url']}">${parent_node['title']}</a>).
    ##      %else:
    ##          There have been no registrations of the parent project (<a href="${parent_node['url']}">${parent_node['title']}</a>).
    ##      %endif
        % else:
        <p>
          There have been no completed registrations of this ${node['node_type']}.
          For a list of the most viewed and most recent public registrations on the
          Open Science Framework, click <a href="/explore/activity/#newPublicRegistrations">here</a>,
          or you start a new draft registration from the "Draft Registrations" tab.
        </p>
        % endif
        %if parent_node['exists'] and user['is_admin_parent']:
        <br />
        <br />
        To register the entire project "${parent_node['title']}" instead, click <a href="${parent_node['registrations_url']}">here.</a>
        %endif
      </div>
      % if 'admin' in user['permissions'] and not disk_saving_mode:
      <div class="col-md-3">
        <a id="registerNode" class="btn btn-default" type="button">
          New Registration
        </a>
      </div>
      % endif
    </div>
  </div>
  <div role="tabpanel" class="tab-pane" id="drafts">
    <div id="draftRegistrationsScope" class="row scripted" style="min-height: 150px;padding-top:20px;">
      <div data-bind="visible: loading" class="spinner-loading-wrapper">
        <div class="logo-spin logo-lg"></div>
      </div>
      <form id="newDraftRegistrationForm" method="POST" style="display:none">
        <!-- ko if: selectedSchema() -->
        <input type="hidden" name="schema_name" data-bind="value: selectedSchema().name">
        <input type="hidden" name="schema_version" data-bind="value: selectedSchema().version">
        <!-- /ko -->
      </form>
      <div>
        <div class="col-md-9">
          <div class="scripted" data-bind="foreach: drafts">
            <li class="project list-group-item list-group-item-node">
              <h4 data-bind="text: schema().title" ></h4>
              <h4 class="list-group-item-heading">
                <div class="progress progress-bar-md">
                  <div class="progress-bar" role="progressbar" aria-valuemin="0" aria-valuemax="100"
                       data-bind="attr.aria-completion: completion,
                                  style: {width: completion() + '%'}">
                    <span class="sr-only"></span>
                  </div>
                </div>
                <small>
                <p>Initiated by: <span data-bind="text: initiator.fullname"></span>
                <p>Started: <span data-bind="text: initiated"></span></p>
                <p>Last updated: <span data-bind="text: updated"></span></p>
                <span data-bind="if: requiresApproval">
                    <div data-bind="if: isApproved">
                        <div class="draft-status-badge bg-success"> Approved</div>
                    </div>
                    <div data-bind="ifnot: isApproved">
                        <div class="draft-status-badge bg-warning"> Pending Approval </div>
                    </div>
                    <div data-bind="if: isPendingReview">
                        <div class="draft-status-badge bg-warning"> Pending Review</div>
                    </div>
                </span>
                </small>
                <div class="row">
                  <div class="col-md-10">
                    <a class="btn btn-info"
                       data-bind="click: $root.editDraft"><i style="margin-right: 5px;" class="fa fa-pencil"></i>Edit</a>
                    <button class="btn btn-danger"
                            data-bind="click: $root.deleteDraft"><i style="margin-right: 5px;" class="fa fa-times"></i>Delete</button>
                  </div>
                  <div class="col-md-1">
                     <a class="btn btn-success" data-bind="attr.href: urls.register_page,
                                                           css: {'disabled': !isApproved}">Register</a>
                  </div>
                </div>
              </h4>
            </li>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</div>
<script type="text/html" id="createDraftRegistrationModal">
    <p>Registration creates a frozen version of the project that can never be edited or deleted but can be retracted. Your original project remains editable but will now have the registration linked to it. Things to know about registration:</p>
    <ul>
        <li>Ensure your project is in the state you wish to freeze before registering.</li>
        <li>Consider turning links into forks.</li>
        <li>Registrations can have embargo periods for up to four years. If you choose an embargo period, the registration will automatically become public when the embargo expires.</li>
        <li>Retracting a registration removes the contents of the registrations but will leave behind a log showing when the registration was created and retracted.</li>
    </ul>

    <p>Continue your registration by selecting a registration form:</p>
    <span data-bind="foreach: schemas">
    <div class="radio">
        <label>
          <input type="radio" name="selectedDraftSchema"
                 data-bind="attr {value: id}, checked: $root.selectedSchemaId" />
          {{ schema.title }}
          <!-- ko if: schema.description -->
          <i data-bind="tooltip: {title: schema.description}" class="fa fa-info-circle"> </i>
          <!-- /ko -->
        </label>
    </div>
    </span>
</script>
<%def name="javascript_bottom()">
    ${parent.javascript_bottom()}

    <script src=${"/static/public/js/project-registrations-page.js" | webpack_asset}> </script>
</%def>

<%include file="project/registration_preview.mako" />
