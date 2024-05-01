# vim:ts=4 sw=4 expandtab softtabstop=4
from jsonschema.validators import RefResolver, urldefrag, urljoin

class LocalRefResolver(RefResolver):
    # We want to have a class that is the same as jsonschema's RefResolver
    # except:
    #
    #  * No caching for resolves. We are changing the schema as we walk through
    #    it, so with caching you can get outdated resolves.
    #
    #  * Provide a _is_remote_ref() method to check if a $ref points to an
    #    external reference.

    def __init__(self, *args, **kwargs):
        kwargs["remote_cache"] = self.resolve_from_url
        super(LocalRefResolver, self).__init__(*args, **kwargs)

    def is_remote_ref(self, ref):
        url = urljoin(self.resolution_scope, ref)
        url, fragment = urldefrag(url)
        return url != self.base_uri
