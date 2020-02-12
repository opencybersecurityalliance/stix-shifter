class SearchFeatureNotSupportedError(NotImplementedError):
    """ Use this error when the current features allowed by the search platform make this feature difficult or
    impossible to implement. For instance, analytics that require subsearches or joins are usually going to be
    un-implementable against NoSQL search platforms like ElasticSearch. In the future, we may develop a client-side
    engine to cover these cases."""
