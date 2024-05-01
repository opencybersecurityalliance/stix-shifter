# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelComposed,
    cached_property,
)


class TimeseriesQuery(ModelComposed):
    def __init__(self, **kwargs):
        """
        An individual timeseries query to one of the basic Datadog data sources.

        :param data_source: A data source that is powered by the Metrics platform.
        :type data_source: MetricsDataSource

        :param name: The variable name for use in formulas.
        :type name: str, optional

        :param query: A classic metrics query string.
        :type query: str

        :param compute: The instructions for what to compute for this query.
        :type compute: EventsCompute

        :param group_by: The list of facets on which to split results.
        :type group_by: EventsQueryGroupBys, optional

        :param indexes: The indexes in which to search.
        :type indexes: [str], optional

        :param search: Configuration of the search/filter for an events query.
        :type search: EventsSearch, optional
        """
        super().__init__(kwargs)

    @cached_property
    def _composed_schemas(_):
        # we need this here to make our import statements work
        # we must store _composed_schemas in here so the code is only run
        # when we invoke this method. If we kept this at the class
        # level we would get an error because the class level
        # code would be run when this module is imported, and these composed
        # classes don't exist yet because their module has not finished
        # loading
        from datadog_api_client.v2.model.metrics_timeseries_query import MetricsTimeseriesQuery
        from datadog_api_client.v2.model.events_timeseries_query import EventsTimeseriesQuery

        return {
            "oneOf": [
                MetricsTimeseriesQuery,
                EventsTimeseriesQuery,
            ],
        }
