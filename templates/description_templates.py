import textwrap

# we might have multiple templates to test, some might be better than others
MESSAGE_TEMPLATE_1 = textwrap.dedent(
    """
    Below is a snippet of a python function:
        {FUNCTION_SNIPPET}    

    Write a json description of this function.
    Return the output as this example:
        {{
            "function_description": {DESCRIPTION_EXAMPLE}
        }}
    Do not return the example!
    """
)

MESSAGE_TEMPLATE_2 = textwrap.dedent(
    """
    ###
    Below is a short summary of a python function in natural language:
        {FUNCTION_SNIPPET}    

    ### 
    Write a description of this function.
    Return the output as this example:
        {{
            "function_snippet": 
            {SNIPPET_EXAMPLE},
            "function_description": {DESCRIPTION_EXAMPLE}
        }}
    """
)


SNIPPET_EXAMPLE_1 = textwrap.dedent(
    """
    def get_current_weather(
        location: str,
        unit: str="fahrenheit"
    ) -> str:
        \"\"\"
        Get the current weather in a given location
        \"\"\"
        <function implementation...>
    """
)

DESCRIPTION_EXAMPLE_1 = textwrap.dedent(
    """
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        }
    """
)

SNIPPET_EXAMPLE_2 = textwrap.dedent(
    '''
def example_function(
    num_tickets: int,
    ticket_type: Dict[str, str]
    event_details: str,
    attendees: List[Dict[str, str]],
) -> Dict[str, float]:
    """
    Orders event tickets and returns the total price.
    
    Parameters:
        num_tickets (int): The number of tickets to buy.
        ticket_type (str): The type of ticket.
        event_details (Dict[str, str]): Details aobut the event, should contain a date in YYYY-MM-DD format.
        passengers (List[Dict[str, str]]): A list of dictionaries containing attendee details.
                                          Each dictionary should have 'name' and 'age' keys.
                                          
    Returns:
        Dict[str, float]: A dictionary with 'total_price' as a key and the total price as a value.
    """
'''
)

DESCRIPTION_EXAMPLE_2 = textwrap.dedent(
    """
{
    "name": "example_function",
    "description": "Orders event tickets and returns the total price.",
    "parameters": {
        "type": "object",
        "properties": {
            "num_tickets": {
                "type": "integer",
                "description": "The number of tickets to buy."
            },
            "ticket_type": {
                "type": "object",
                "description": "The type of ticket.",
                "properties": {
                    "type": "string"
                }
            },
            "event_details": {
                "type": "object",
                "description": "Details about the event, should contain a date in YYYY-MM-DD format.",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "Event data in YYYY-MM-DD format."
                    }
                },
                "required": ["date"]
            },
            "attendees": {
                "type": "array",
                "description": "A list of dictionaries containing attendee details. Each dictionary should have 'name' and 'age' keys.",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string"
                        },
                        "age": {
                            "type": "string"
                        }
                    },
                    "required": ["name", "age"]
                }
            }
        },
        "required": ["num_tickets", "ticket_type", "event_details", "attendees"]
    },
    "returns": {
        "type": "object",
        "properties": {
            "total_price": {
                "type": "float",
                "description": "The total price for the tickets ordered."
            }
        }
    }
}
"""
)
