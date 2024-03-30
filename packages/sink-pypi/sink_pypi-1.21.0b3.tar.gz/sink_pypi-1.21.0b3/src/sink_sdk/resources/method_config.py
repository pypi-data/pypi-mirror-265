# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from ..types import (
    Card,
    MethodConfigSkippedTestsGoResponse,
    MethodConfigSkippedTestsAllResponse,
    MethodConfigSkippedTestsJavaResponse,
    MethodConfigSkippedTestsNodeResponse,
    MethodConfigSkippedTestsRubyResponse,
    MethodConfigSkippedTestsKotlinResponse,
    MethodConfigSkippedTestsPythonResponse,
    MethodConfigSkippedTestsNodeAndPythonResponse,
    shared_params,
    method_config_should_not_show_up_in_api_docs_params,
)
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

__all__ = ["MethodConfig", "AsyncMethodConfig"]


class MethodConfig(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> MethodConfigWithRawResponse:
        return MethodConfigWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MethodConfigWithStreamingResponse:
        return MethodConfigWithStreamingResponse(self)

    def should_not_show_up_in_api_docs(
        self,
        card_token: str,
        *,
        product_id: str | NotGiven = NOT_GIVEN,
        shipping_method: Literal["STANDARD", "STANDARD_WITH_TRACKING", "EXPEDITED"] | NotGiven = NOT_GIVEN,
        shipping_address: shared_params.ShippingAddress | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> Card:
        """
        Initiate print and shipment of a duplicate card.

        Only applies to cards of type `PHYSICAL` [beta].

        Args:
          product_id: Specifies the configuration (e.g. physical card art) that the card should be
              manufactured with, and only applies to cards of type `PHYSICAL` [beta]. This
              must be configured with Lithic before use.

          shipping_method: Shipping method for the card. Use of options besides `STANDARD` require
              additional permissions.

              - `STANDARD` - USPS regular mail or similar international option, with no
                tracking
              - `STANDARD_WITH_TRACKING` - USPS regular mail or similar international option,
                with tracking
              - `EXPEDITED` - FedEx Standard Overnight or similar international option, with
                tracking

          shipping_address: If omitted, the previous shipping address will be used.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not card_token:
            raise ValueError(f"Expected a non-empty value for `card_token` but received {card_token!r}")
        return self._post(
            f"/cards/{card_token}/reissue",
            body=maybe_transform(
                {
                    "product_id": product_id,
                    "shipping_method": shipping_method,
                    "shipping_address": shipping_address,
                },
                method_config_should_not_show_up_in_api_docs_params.MethodConfigShouldNotShowUpInAPIDocsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=Card,
        )

    def skipped_tests_all(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MethodConfigSkippedTestsAllResponse:
        """
        Used to test skipping generated unit tests.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/method_config/skipped_tests/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MethodConfigSkippedTestsAllResponse,
        )

    def skipped_tests_go(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MethodConfigSkippedTestsGoResponse:
        """
        Used to test skipping generated unit tests.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/method_config/skipped_tests/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MethodConfigSkippedTestsGoResponse,
        )

    def skipped_tests_java(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MethodConfigSkippedTestsJavaResponse:
        """
        Used to test skipping generated unit tests.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/method_config/skipped_tests/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MethodConfigSkippedTestsJavaResponse,
        )

    def skipped_tests_kotlin(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MethodConfigSkippedTestsKotlinResponse:
        """
        Used to test skipping generated unit tests.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/method_config/skipped_tests/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MethodConfigSkippedTestsKotlinResponse,
        )

    def skipped_tests_node(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MethodConfigSkippedTestsNodeResponse:
        """
        Used to test skipping generated unit tests.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/method_config/skipped_tests/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MethodConfigSkippedTestsNodeResponse,
        )

    def skipped_tests_node_and_python(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MethodConfigSkippedTestsNodeAndPythonResponse:
        """
        Used to test skipping generated unit tests.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/method_config/skipped_tests/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MethodConfigSkippedTestsNodeAndPythonResponse,
        )

    def skipped_tests_python(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MethodConfigSkippedTestsPythonResponse:
        """
        Used to test skipping generated unit tests.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/method_config/skipped_tests/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MethodConfigSkippedTestsPythonResponse,
        )

    def skipped_tests_ruby(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MethodConfigSkippedTestsRubyResponse:
        """
        Used to test skipping generated unit tests.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/method_config/skipped_tests/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MethodConfigSkippedTestsRubyResponse,
        )


class AsyncMethodConfig(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncMethodConfigWithRawResponse:
        return AsyncMethodConfigWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMethodConfigWithStreamingResponse:
        return AsyncMethodConfigWithStreamingResponse(self)

    async def should_not_show_up_in_api_docs(
        self,
        card_token: str,
        *,
        product_id: str | NotGiven = NOT_GIVEN,
        shipping_method: Literal["STANDARD", "STANDARD_WITH_TRACKING", "EXPEDITED"] | NotGiven = NOT_GIVEN,
        shipping_address: shared_params.ShippingAddress | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> Card:
        """
        Initiate print and shipment of a duplicate card.

        Only applies to cards of type `PHYSICAL` [beta].

        Args:
          product_id: Specifies the configuration (e.g. physical card art) that the card should be
              manufactured with, and only applies to cards of type `PHYSICAL` [beta]. This
              must be configured with Lithic before use.

          shipping_method: Shipping method for the card. Use of options besides `STANDARD` require
              additional permissions.

              - `STANDARD` - USPS regular mail or similar international option, with no
                tracking
              - `STANDARD_WITH_TRACKING` - USPS regular mail or similar international option,
                with tracking
              - `EXPEDITED` - FedEx Standard Overnight or similar international option, with
                tracking

          shipping_address: If omitted, the previous shipping address will be used.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not card_token:
            raise ValueError(f"Expected a non-empty value for `card_token` but received {card_token!r}")
        return await self._post(
            f"/cards/{card_token}/reissue",
            body=await async_maybe_transform(
                {
                    "product_id": product_id,
                    "shipping_method": shipping_method,
                    "shipping_address": shipping_address,
                },
                method_config_should_not_show_up_in_api_docs_params.MethodConfigShouldNotShowUpInAPIDocsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=Card,
        )

    async def skipped_tests_all(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MethodConfigSkippedTestsAllResponse:
        """
        Used to test skipping generated unit tests.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/method_config/skipped_tests/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MethodConfigSkippedTestsAllResponse,
        )

    async def skipped_tests_go(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MethodConfigSkippedTestsGoResponse:
        """
        Used to test skipping generated unit tests.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/method_config/skipped_tests/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MethodConfigSkippedTestsGoResponse,
        )

    async def skipped_tests_java(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MethodConfigSkippedTestsJavaResponse:
        """
        Used to test skipping generated unit tests.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/method_config/skipped_tests/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MethodConfigSkippedTestsJavaResponse,
        )

    async def skipped_tests_kotlin(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MethodConfigSkippedTestsKotlinResponse:
        """
        Used to test skipping generated unit tests.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/method_config/skipped_tests/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MethodConfigSkippedTestsKotlinResponse,
        )

    async def skipped_tests_node(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MethodConfigSkippedTestsNodeResponse:
        """
        Used to test skipping generated unit tests.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/method_config/skipped_tests/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MethodConfigSkippedTestsNodeResponse,
        )

    async def skipped_tests_node_and_python(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MethodConfigSkippedTestsNodeAndPythonResponse:
        """
        Used to test skipping generated unit tests.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/method_config/skipped_tests/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MethodConfigSkippedTestsNodeAndPythonResponse,
        )

    async def skipped_tests_python(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MethodConfigSkippedTestsPythonResponse:
        """
        Used to test skipping generated unit tests.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/method_config/skipped_tests/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MethodConfigSkippedTestsPythonResponse,
        )

    async def skipped_tests_ruby(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MethodConfigSkippedTestsRubyResponse:
        """
        Used to test skipping generated unit tests.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/method_config/skipped_tests/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MethodConfigSkippedTestsRubyResponse,
        )


class MethodConfigWithRawResponse:
    def __init__(self, method_config: MethodConfig) -> None:
        self._method_config = method_config

        self.should_not_show_up_in_api_docs = to_raw_response_wrapper(
            method_config.should_not_show_up_in_api_docs,
        )
        self.skipped_tests_all = to_raw_response_wrapper(
            method_config.skipped_tests_all,
        )
        self.skipped_tests_go = to_raw_response_wrapper(
            method_config.skipped_tests_go,
        )
        self.skipped_tests_java = to_raw_response_wrapper(
            method_config.skipped_tests_java,
        )
        self.skipped_tests_kotlin = to_raw_response_wrapper(
            method_config.skipped_tests_kotlin,
        )
        self.skipped_tests_node = to_raw_response_wrapper(
            method_config.skipped_tests_node,
        )
        self.skipped_tests_node_and_python = to_raw_response_wrapper(
            method_config.skipped_tests_node_and_python,
        )
        self.skipped_tests_python = to_raw_response_wrapper(
            method_config.skipped_tests_python,
        )
        self.skipped_tests_ruby = to_raw_response_wrapper(
            method_config.skipped_tests_ruby,
        )


class AsyncMethodConfigWithRawResponse:
    def __init__(self, method_config: AsyncMethodConfig) -> None:
        self._method_config = method_config

        self.should_not_show_up_in_api_docs = async_to_raw_response_wrapper(
            method_config.should_not_show_up_in_api_docs,
        )
        self.skipped_tests_all = async_to_raw_response_wrapper(
            method_config.skipped_tests_all,
        )
        self.skipped_tests_go = async_to_raw_response_wrapper(
            method_config.skipped_tests_go,
        )
        self.skipped_tests_java = async_to_raw_response_wrapper(
            method_config.skipped_tests_java,
        )
        self.skipped_tests_kotlin = async_to_raw_response_wrapper(
            method_config.skipped_tests_kotlin,
        )
        self.skipped_tests_node = async_to_raw_response_wrapper(
            method_config.skipped_tests_node,
        )
        self.skipped_tests_node_and_python = async_to_raw_response_wrapper(
            method_config.skipped_tests_node_and_python,
        )
        self.skipped_tests_python = async_to_raw_response_wrapper(
            method_config.skipped_tests_python,
        )
        self.skipped_tests_ruby = async_to_raw_response_wrapper(
            method_config.skipped_tests_ruby,
        )


class MethodConfigWithStreamingResponse:
    def __init__(self, method_config: MethodConfig) -> None:
        self._method_config = method_config

        self.should_not_show_up_in_api_docs = to_streamed_response_wrapper(
            method_config.should_not_show_up_in_api_docs,
        )
        self.skipped_tests_all = to_streamed_response_wrapper(
            method_config.skipped_tests_all,
        )
        self.skipped_tests_go = to_streamed_response_wrapper(
            method_config.skipped_tests_go,
        )
        self.skipped_tests_java = to_streamed_response_wrapper(
            method_config.skipped_tests_java,
        )
        self.skipped_tests_kotlin = to_streamed_response_wrapper(
            method_config.skipped_tests_kotlin,
        )
        self.skipped_tests_node = to_streamed_response_wrapper(
            method_config.skipped_tests_node,
        )
        self.skipped_tests_node_and_python = to_streamed_response_wrapper(
            method_config.skipped_tests_node_and_python,
        )
        self.skipped_tests_python = to_streamed_response_wrapper(
            method_config.skipped_tests_python,
        )
        self.skipped_tests_ruby = to_streamed_response_wrapper(
            method_config.skipped_tests_ruby,
        )


class AsyncMethodConfigWithStreamingResponse:
    def __init__(self, method_config: AsyncMethodConfig) -> None:
        self._method_config = method_config

        self.should_not_show_up_in_api_docs = async_to_streamed_response_wrapper(
            method_config.should_not_show_up_in_api_docs,
        )
        self.skipped_tests_all = async_to_streamed_response_wrapper(
            method_config.skipped_tests_all,
        )
        self.skipped_tests_go = async_to_streamed_response_wrapper(
            method_config.skipped_tests_go,
        )
        self.skipped_tests_java = async_to_streamed_response_wrapper(
            method_config.skipped_tests_java,
        )
        self.skipped_tests_kotlin = async_to_streamed_response_wrapper(
            method_config.skipped_tests_kotlin,
        )
        self.skipped_tests_node = async_to_streamed_response_wrapper(
            method_config.skipped_tests_node,
        )
        self.skipped_tests_node_and_python = async_to_streamed_response_wrapper(
            method_config.skipped_tests_node_and_python,
        )
        self.skipped_tests_python = async_to_streamed_response_wrapper(
            method_config.skipped_tests_python,
        )
        self.skipped_tests_ruby = async_to_streamed_response_wrapper(
            method_config.skipped_tests_ruby,
        )
