 <div id="s3Scope" class="scripted">

    <!-- Add credentials modal -->
    <%include file="s3_credentials_modal.mako"/>

    <h4 class="addon-title">
        <img class="addon-icon" src="${addon_icon_url}">
        Amazon S3
        <small class="authorized-by">
            <span data-bind="if: nodeHasAuth">
                authorized by <a data-bind="attr: {href: urls().owner}, text: ownerName"></a>
                % if not is_registration:
                    <a data-bind="click: deauthorizeNode" class="text-danger pull-right addon-auth">
                      Disconnect Account
                    </a>
                % endif
            </span>
            <span data-bind="if: showImport">
                <a data-bind="click: importAuth" class="text-primary pull-right addon-auth">
                  Import Account from Profile
                </a>
            </span>
            <span data-bind="if: showCreateCredentials">
                <a href="#s3InputCredentials" data-toggle="modal" class="pull-right text-primary addon-auth">
                    Connect  Account
                </a>
            </span>
        </small>
    </h4>
    <div data-bind="if: showSettings">
      <div class="row">
      <div class="col-md-12">
        <p>
          <strong>Current Bucket:</strong>
          <span data-bind="ifnot: currentBucket">
            None
          </span>
          <a data-bind="if: currentBucket, attr: {href: urls().files}">
              <span data-bind="text: currentBucket"></span>
          </a>
        </p>
        <div data-bind="attr: {disabled: creating}">
          <button data-bind="visible: canChange, click: toggleSelect,
                             css: {active: showSelect}" class="btn btn-primary">Change</button>
          <button data-bind="visible: showNewBucket, click: openCreateBucket,
                             attr: {disabled: creating}" class="btn btn-success" id="newBucket">Create Bucket</button>
        </div>
        <br />
        <br />
        <div class="row" data-bind="if: showSelect">
          <div class="form-group col-md-8">
            <select class="form-control" id="s3_bucket" name="s3_bucket"
                    data-bind="value: selectedBucket,
                               attr: {disabled: !loadedBucketList()},
                               options: bucketList"> </select>
          </div>
          ## Remove comments to enable user toggling of file upload encryption
          ## <div class="col-md-3">
          ##   <input type="checkbox" id="encryptUploads" name="encryptUploads"
          ##         data-bind="checked: encryptUploads" />  Encrypt file uploads
          ## </div>
          <div class="col-md-2">
            <button data-bind="click: selectBucket,
                               attr: {disabled: !allowSelectBucket()},
                               text: saveButtonText"
                    class="btn btn-success">
              Save
            </button>
          </div>
        </div>
      </div>
      </div>
    </div>
    <!-- Flashed Messages -->
    <div class="help-block">
        <p data-bind="html: node_message, attr: {class: messageClass}"></p>
    </div>
</div>
