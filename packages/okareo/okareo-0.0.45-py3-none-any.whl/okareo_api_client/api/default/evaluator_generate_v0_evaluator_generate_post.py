from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.evaluator_generate_response import EvaluatorGenerateResponse
from ...models.evaluator_spec_request import EvaluatorSpecRequest
from ...types import Response


def _get_kwargs(
    *,
    json_body: EvaluatorSpecRequest,
    api_key: str,
) -> Dict[str, Any]:
    headers = {}
    headers["api-key"] = api_key

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/v0/evaluator_generate",
        "json": json_json_body,
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponse, EvaluatorGenerateResponse]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = EvaluatorGenerateResponse.from_dict(response.json())

        return response_201
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = ErrorResponse.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[ErrorResponse, EvaluatorGenerateResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: EvaluatorSpecRequest,
    api_key: str,
) -> Response[Union[ErrorResponse, EvaluatorGenerateResponse]]:
    """Evaluator Generate

     Generate code for an evaluator for testing.
    Returns:
        the evaluator object with the generated code

    Args:
        api_key (str):
        json_body (EvaluatorSpecRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, EvaluatorGenerateResponse]]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
        api_key=api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: EvaluatorSpecRequest,
    api_key: str,
) -> Optional[Union[ErrorResponse, EvaluatorGenerateResponse]]:
    """Evaluator Generate

     Generate code for an evaluator for testing.
    Returns:
        the evaluator object with the generated code

    Args:
        api_key (str):
        json_body (EvaluatorSpecRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, EvaluatorGenerateResponse]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        api_key=api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: EvaluatorSpecRequest,
    api_key: str,
) -> Response[Union[ErrorResponse, EvaluatorGenerateResponse]]:
    """Evaluator Generate

     Generate code for an evaluator for testing.
    Returns:
        the evaluator object with the generated code

    Args:
        api_key (str):
        json_body (EvaluatorSpecRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, EvaluatorGenerateResponse]]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
        api_key=api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: EvaluatorSpecRequest,
    api_key: str,
) -> Optional[Union[ErrorResponse, EvaluatorGenerateResponse]]:
    """Evaluator Generate

     Generate code for an evaluator for testing.
    Returns:
        the evaluator object with the generated code

    Args:
        api_key (str):
        json_body (EvaluatorSpecRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, EvaluatorGenerateResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            api_key=api_key,
        )
    ).parsed
