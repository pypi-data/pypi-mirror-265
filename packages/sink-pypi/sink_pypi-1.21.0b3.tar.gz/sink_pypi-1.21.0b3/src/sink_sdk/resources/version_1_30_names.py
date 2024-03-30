# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import Version1_30NameCreateResponse, version_1_30_name_create_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import (
    make_request_options,
)

__all__ = ["Version1_30Names", "AsyncVersion1_30Names"]


class Version1_30Names(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> Version1_30NamesWithRawResponse:
        return Version1_30NamesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> Version1_30NamesWithStreamingResponse:
        return Version1_30NamesWithStreamingResponse(self)

    def create(
        self,
        version_1_15: str | NotGiven = NOT_GIVEN,
        *,
        version_1_16: str | NotGiven = NOT_GIVEN,
        version_1_17: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> Version1_30NameCreateResponse:
        """
        The `X-Client-Secret` header shouldn't be included in params definitions as it
        is already sent as a client argument.

        Whereas the `X-Custom-Endpoint-Header` should be included as it is only used
        here.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not version_1_15:
            raise ValueError(f"Expected a non-empty value for `version_1_15` but received {version_1_15!r}")
        return self._post(
            f"/version_1_30_names/query/{version_1_15}",
            body=maybe_transform(
                {"version_1_17": version_1_17}, version_1_30_name_create_params.Version1_30NameCreateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
                query=maybe_transform(
                    {"version_1_16": version_1_16}, version_1_30_name_create_params.Version1_30NameCreateParams
                ),
            ),
            cast_to=Version1_30NameCreateResponse,
        )


class AsyncVersion1_30Names(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncVersion1_30NamesWithRawResponse:
        return AsyncVersion1_30NamesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncVersion1_30NamesWithStreamingResponse:
        return AsyncVersion1_30NamesWithStreamingResponse(self)

    async def create(
        self,
        version_1_15: str | NotGiven = NOT_GIVEN,
        *,
        version_1_16: str | NotGiven = NOT_GIVEN,
        version_1_17: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> Version1_30NameCreateResponse:
        """
        The `X-Client-Secret` header shouldn't be included in params definitions as it
        is already sent as a client argument.

        Whereas the `X-Custom-Endpoint-Header` should be included as it is only used
        here.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not version_1_15:
            raise ValueError(f"Expected a non-empty value for `version_1_15` but received {version_1_15!r}")
        return await self._post(
            f"/version_1_30_names/query/{version_1_15}",
            body=await async_maybe_transform(
                {"version_1_17": version_1_17}, version_1_30_name_create_params.Version1_30NameCreateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
                query=await async_maybe_transform(
                    {"version_1_16": version_1_16}, version_1_30_name_create_params.Version1_30NameCreateParams
                ),
            ),
            cast_to=Version1_30NameCreateResponse,
        )


class Version1_30NamesWithRawResponse:
    def __init__(self, version_1_30_names: Version1_30Names) -> None:
        self._version_1_30_names = version_1_30_names

        self.create = to_raw_response_wrapper(
            version_1_30_names.create,
        )


class AsyncVersion1_30NamesWithRawResponse:
    def __init__(self, version_1_30_names: AsyncVersion1_30Names) -> None:
        self._version_1_30_names = version_1_30_names

        self.create = async_to_raw_response_wrapper(
            version_1_30_names.create,
        )


class Version1_30NamesWithStreamingResponse:
    def __init__(self, version_1_30_names: Version1_30Names) -> None:
        self._version_1_30_names = version_1_30_names

        self.create = to_streamed_response_wrapper(
            version_1_30_names.create,
        )


class AsyncVersion1_30NamesWithStreamingResponse:
    def __init__(self, version_1_30_names: AsyncVersion1_30Names) -> None:
        self._version_1_30_names = version_1_30_names

        self.create = async_to_streamed_response_wrapper(
            version_1_30_names.create,
        )
