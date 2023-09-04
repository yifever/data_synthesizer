import textwrap

# we might have multiple templates to test, some might be better than others
MESSAGE_TEMPLATE_1 = textwrap.dedent(
    """
    Below is the description of a function:
        "function_description":
        {FUNCTION_DESCRIPTION}

    Write a user prompt that would call this function, and the function call.
    Return the output as this example:
        {{
            "function_description":
            {FUNCTION_EXAMPLE},
            "user_prompt": {PROMPT_EXAMPLE},
            "function_call": {CALL_EXAMPLE}
        }}
    """
)

MESSAGE_TEMPLATE_2 = textwrap.dedent(
    """
    Below is the description of a function:
        "function_description":
        {FUNCTION_DESCRIPTION}


    A user is asking an assisstant a request that would eventually call the function, can you write that conversation for me.
    Return the output as this example:
        {{
            "conversation": {PROMPT_EXAMPLE},
            "function_call": {CALL_EXAMPLE}
        }}
    """
)

PROMPT_EXAMPLE_1 = textwrap.dedent(
    """
    "what is the weather going to be like in Glasgow, Scotland over the next 7 days"
    """
)

FUNCTION_EXAMPLE_1 = textwrap.dedent(
    """
    {
        "name": "get_n_day_weather_forecast",
        "description": "Get an N-day weather forecast",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                },
                "format": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "The temperature unit to use. Infer this from the users location.",
                },
                "num_days": {
                    "type": "integer",
                    "description": "The number of days to forecast",
                }
            },
            "required": ["location", "format", "num_days"]
        },
    }
    """
)

CALL_EXAMPLE_1 = textwrap.dedent(
    """
    {
        "name": "get_n_day_weather_forecast",
        "arguments": "{\n  "location": "Glasgow, Scotland",\n  "format": "celsius",\n  "num_days": 5\n}"
    }
    """
)

FUNCTION_EXAMPLE_2 = textwrap.dedent(
    """
    "function_description": {
        "name": "example_function",
        "description": "Retrieves a user's timeline, including tweets, retweets, and replies.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The ID of the user."
                }
            },
            "required": ["user_id"]
        },
        "returns": {
            "type": "object",
            "properties": {
                "tweet_id": {"type": "string"},
                "text": {"type": "string"},
                "author": {"type": "string"},
                "date": {"type": "string"}
            }
        }
    }
    """
)

CONVERSATION_EXAMPLE_2 = textwrap.dedent(
    """
    [
        {
            "role": "user",
            "text": "Hey, can you show me my Twitter timeline?"
        },
        {
            "role": "assistant",
            "text": "Sure, I can do that. May I know your Twitter user ID?"
        },
        {
            "role": "user",
            "text": "Yes, my Twitter user ID is '13579'."
        },
        {
            "role": "assistant",
            "text": "Great, I'm retrieving your Twitter timeline now."
        }
    ]
    """
)

CALL_EXAMPLE_2 = textwrap.dedent(
    """
    {
        "function_name": "example_function",
        "parameters": {
            "user_id": "13579"
        }
    }
    """
)
