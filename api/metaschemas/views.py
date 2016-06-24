from modularodm import Q
from rest_framework import generics, permissions as drf_permissions
from rest_framework.exceptions import NotFound

from framework.auth.oauth_scopes import CoreScopes

from website.project.metadata.schemas import ACTIVE_META_SCHEMAS, LATEST_SCHEMA_VERSION
from api.base import permissions as base_permissions
from api.base.views import JSONAPIBaseView
from api.base.utils import get_object_or_error

from website.models import MetaSchema
from api.metaschemas.serializers import MetaSchemaSerializer


class MetaSchemasList(JSONAPIBaseView, generics.ListAPIView):
    """
     <!--- Copied from MetaSchemaDetail -->

    Metaschemas describe the supplemental questions that accompany a registration.
    Only active metaschemas are returned at this endpoint.

    ##Metaschema Attributes

    Metaschemas have the "metaschemas" `type`.

        name                type               description
        ===========================================================================
        name                string             name of registration schema
        schema_version      integer            latest version of the schema
        schema              dictionary         registration schema details


    ##Links`

    See the [JSON-API spec regarding pagination](http://jsonapi.org/format/1.0/#fetching-pagination).

    #This request/response

    """
    permission_classes = (
        drf_permissions.IsAuthenticatedOrReadOnly,
        base_permissions.TokenHasScope,
    )

    required_read_scopes = [CoreScopes.NODE_DRAFT_REGISTRATIONS_READ]
    required_write_scopes = [CoreScopes.NODE_DRAFT_REGISTRATIONS_WRITE]

    serializer_class = MetaSchemaSerializer
    view_category = 'metaschemas'
    view_name = 'metaschema-list'

    # overrides ListCreateAPIView
    def get_queryset(self):
        schemas = MetaSchema.find(Q('name', 'in', ACTIVE_META_SCHEMAS) &
                                  Q('schema_version', 'eq', LATEST_SCHEMA_VERSION))
        return schemas


class MetaSchemaDetail(JSONAPIBaseView, generics.RetrieveAPIView):
    """
    Metaschemas describe the supplemental questions that accompany a registration.

    ##Metaschema Attributes

    Metaschemas have the "metaschemas" `type`.

         name                type               description
        ===========================================================================
        name                string             name of registration schema
        schema_version      integer            latest version of the schema
        schema              dictionary         registration schema details

    #This request/response

    """
    permission_classes = (
        drf_permissions.IsAuthenticatedOrReadOnly,
        base_permissions.TokenHasScope,
    )

    required_read_scopes = [CoreScopes.METASCHEMA_READ]
    required_write_scopes = [CoreScopes.NULL]

    serializer_class = MetaSchemaSerializer
    view_category = 'metaschemas'
    view_name = 'metaschema-detail'

    # overrides RetrieveAPIView
    def get_object(self):
        schema_id = self.kwargs['metaschema_id']
        schema = get_object_or_error(MetaSchema, schema_id)
        if schema.schema_version != LATEST_SCHEMA_VERSION or schema.name not in ACTIVE_META_SCHEMAS:
            raise NotFound
        return schema
