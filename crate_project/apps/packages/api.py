from django.conf.urls import include, url

from tastypie import fields
from tastypie.bundle import Bundle
from tastypie.cache import SimpleCache
from tastypie.constants import ALL
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash

from packages.models import Package, Release


class PackageResource(ModelResource):
    releases = fields.ToManyField("packages.api.ReleaseResource", "releases")

    class Meta:
        allowed_methods = ["get"]
        cache = SimpleCache()
        fields = ["created", "downloads_synced_on", "name"]
        filtering = {
            "name": ALL,
            "created": ALL,
            "downloads_synced_on": ALL,
        }
        include_absolute_url = True
        queryset = Package.objects.all()
        resource_name = "package"

    def override_urls(self):
        rr = ReleaseResource()
        return [
            url(r"^(?P<resource_name>%s)/(?P<name>[^/]+)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view("dispatch_detail"), name="api_dispatch_detail"),
            url(r"^(?P<resource_name>%s)%s" % (self._meta.resource_name, trailing_slash()), include(rr.urls)),
        ]

    def get_resource_uri(self, bundle_or_obj):
        kwargs = {
            "resource_name": self._meta.resource_name,
        }

        if isinstance(bundle_or_obj, Bundle):
            kwargs["name"] = bundle_or_obj.obj.name
        else:
            kwargs["name"] = bundle_or_obj.name

        if self._meta.api_name is not None:
            kwargs["api_name"] = self._meta.api_name

        return self._build_reverse_url("api_dispatch_detail", kwargs=kwargs)


class ReleaseResource(ModelResource):
    package = fields.ForeignKey(PackageResource, "package")

    class Meta:
        allowed_methods = ["get"]
        cache = SimpleCache()
        fields = [
                    "author", "author_email", "created", "description", "download_uri",
                    "license", "maintainer", "maintainer_email", "package", "platform",
                    "requires_python", "summary", "version"
                ]
        include_absolute_url = True
        queryset = Release.objects.all()
        resource_name = "release"

    def base_urls(self):
        """
        The standard URLs this ``Resource`` should respond to.
        """
        # Due to the way Django parses URLs, ``get_multiple`` won't work without
        # a trailing slash.
        return [
            url(r"^schema%s$" % trailing_slash(), self.wrap_view('get_schema'), name="api_get_schema"),
            url(r"^set/(?P<pk_list>\w[\w/;-]*)/$", self.wrap_view('get_multiple'), name="api_get_multiple"),
            url(r"^(?P<package__name>[^/]+)/(?P<version>[^/]+)/$", self.wrap_view("dispatch_detail"), name="api_dispatch_detail"),
        ]

    def get_resource_uri(self, bundle_or_obj):
        kwargs = {
            "resource_name": "package",  # @@@ Might be a better way?
        }

        if isinstance(bundle_or_obj, Bundle):
            kwargs["package__name"] = bundle_or_obj.obj.package.name
            kwargs["version"] = bundle_or_obj.obj.version
        else:
            kwargs["name"] = bundle_or_obj.package.name
            kwargs["version"] = bundle_or_obj.version

        if self._meta.api_name is not None:
            kwargs["api_name"] = self._meta.api_name

        return self._build_reverse_url("api_dispatch_detail", kwargs=kwargs)
