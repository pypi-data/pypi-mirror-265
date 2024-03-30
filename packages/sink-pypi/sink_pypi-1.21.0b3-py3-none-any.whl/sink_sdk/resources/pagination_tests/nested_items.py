# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ...types import MyModel
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...pagination import SyncPageCursorNestedItems, AsyncPageCursorNestedItems
from ..._base_client import (
    AsyncPaginator,
    make_request_options,
)
from ...types.pagination_tests import nested_item_list_params

__all__ = ["NestedItems", "AsyncNestedItems"]


class NestedItems(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> NestedItemsWithRawResponse:
        return NestedItemsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> NestedItemsWithStreamingResponse:
        return NestedItemsWithStreamingResponse(self)

    def list(
        self,
        *,
        cursor: Optional[str] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncPageCursorNestedItems[MyModel]:
        """
        Test case for response headers with cursor pagination

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/paginated/nested_items",
            page=SyncPageCursorNestedItems[MyModel],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "cursor": cursor,
                        "limit": limit,
                    },
                    nested_item_list_params.NestedItemListParams,
                ),
            ),
            model=MyModel,
        )


class AsyncNestedItems(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncNestedItemsWithRawResponse:
        return AsyncNestedItemsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncNestedItemsWithStreamingResponse:
        return AsyncNestedItemsWithStreamingResponse(self)

    def list(
        self,
        *,
        cursor: Optional[str] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncPaginator[MyModel, AsyncPageCursorNestedItems[MyModel]]:
        """
        Test case for response headers with cursor pagination

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/paginated/nested_items",
            page=AsyncPageCursorNestedItems[MyModel],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "cursor": cursor,
                        "limit": limit,
                    },
                    nested_item_list_params.NestedItemListParams,
                ),
            ),
            model=MyModel,
        )


class NestedItemsWithRawResponse:
    def __init__(self, nested_items: NestedItems) -> None:
        self._nested_items = nested_items

        self.list = to_raw_response_wrapper(
            nested_items.list,
        )


class AsyncNestedItemsWithRawResponse:
    def __init__(self, nested_items: AsyncNestedItems) -> None:
        self._nested_items = nested_items

        self.list = async_to_raw_response_wrapper(
            nested_items.list,
        )


class NestedItemsWithStreamingResponse:
    def __init__(self, nested_items: NestedItems) -> None:
        self._nested_items = nested_items

        self.list = to_streamed_response_wrapper(
            nested_items.list,
        )


class AsyncNestedItemsWithStreamingResponse:
    def __init__(self, nested_items: AsyncNestedItems) -> None:
        self._nested_items = nested_items

        self.list = async_to_streamed_response_wrapper(
            nested_items.list,
        )
