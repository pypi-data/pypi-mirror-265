"""An example using the basics of the Fixpoint SDK."""

# pylint: disable=unused-variable
from fixpoint_sdk.client import ChatRouterClient
from fixpoint_sdk.openapi.gen import openapi_client
from fixpoint_sdk.openapi.gen.openapi_client.rest import ApiException
from fixpoint_sdk import FixpointClient, ThumbsReaction


def main() -> None:
    """An example of using FixpointClient to make LLM calls and record feedback."""

    # Make sure that the enviroment variables set:
    # - `FIXPOINT_API_KEY` is set to your Fixpoint API key
    # - `OPENAI_API_KEY` is set to your normal OpenAI API key
    # Create a FixpointClient instance (uses the FIXPOINT_API_KEY env var)
    client = FixpointClient()

    # Call create method on FixpointClient instance. You can specify a user to
    # associate with the request. The user will be automatically passed through
    # to OpenAI's API.
    resp1 = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What are you?"},
        ],
        user="some-user-id",
    )
    openai_response = resp1.completion
    fixpoint_input_log_response = resp1.input_log
    fixpoint_output_log_response = resp1.output_log

    # If you make multiple calls to an LLM that are all part of the same "trace"
    # (e.g. a multi-step chain of prompts), you can pass in a trace_id to
    # associate them together.
    resp2 = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What are you?"},
        ],
        trace_id="some-trace-id",
    )

    # You can use the Fixpoint API in different environment modes: "test",
    # "staging", and "prod".
    # This is useful to make sure that your logged production traffic does not
    # get cluttered with test data or staging data.
    # If you do not specify a mode, we default to "prod".
    for env_mode in ["test", "staging", "prod"]:
        client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            mode=env_mode,
            messages=[
                {
                    "role": "system",
                    "content": f"You are a helpful assistant running in {env_mode} mode.",
                },
                {"role": "user", "content": "What are you?"},
            ],
        )

    # Record user feedback. One user giving a thumbs up to a log, the other giving a thumbs down.
    # The `user_id` you specify should be your own system's user identifier for
    # whoever gave the feedback.
    client.fixpoint.user_feedback.create(
        {
            "likes": [
                {
                    "log_name": fixpoint_input_log_response["name"],
                    "thumbs_reaction": ThumbsReaction.THUMBS_UP,
                    "user_id": "some-user-id",
                },
                {
                    "log_name": resp2.input_log["name"],
                    "thumbs_reaction": ThumbsReaction.THUMBS_DOWN,
                    "user_id": "some-other-user-id",
                },
            ]
        }
    )

    # Record an attribute
    client.fixpoint.attributes.create(
        {
            "log_attribute": {
                "log_name": fixpoint_input_log_response["name"],
                "key": "conversion",
                "value": "true",
            }
        }
    )

    # Define routing configuration
    routing_config = openapi_client.V1CreateRoutingConfigRequest(
        id="123",
        fallback_strategy=openapi_client.V1FallbackStrategy.FALLBACK_STRATEGY_NEXT,
        terminal_state=openapi_client.V1TerminalState.TERMINAL_STATE_ERROR,
        models=[
            openapi_client.V1Model(
                provider="openai",
                name="gpt-3.5-turbo-0125",
                spend_cap=openapi_client.V1SpendCap(
                    amount="0.0001",
                    currency="USD",
                    reset_interval=openapi_client.V1ResetInterval.RESET_INTERVAL_MONTHLY,
                ),
            ),
            openapi_client.V1Model(
                provider="openai",
                name="gpt-3.5-turbo-0301",
                spend_cap=openapi_client.V1SpendCap(
                    amount="0.0001",
                    currency="USD",
                    reset_interval=openapi_client.V1ResetInterval.RESET_INTERVAL_MONTHLY,
                ),
            ),
        ],
        description="This is a test routing config.",
    )

    try:
        api_response = client.fixpoint.proxy_client.llm_proxy_create_routing_config(
            routing_config
        )
    except ApiException as e:
        print(
            f"Exception when calling LLMProxyApi->llm_proxy_create_routing_config: {e}\n"
        )

    client_with_router = ChatRouterClient()

    try:
        api_response = client_with_router.chat.completions.create(
            mode="test",
            user="some-user-id",
            trace_id="some-trace-id",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What are you?"},
            ],
        )
    except ApiException as e:
        print(f"Exception when calling ChatCompletionsApi->create: {e}\n")


if __name__ == "__main__":
    main()
