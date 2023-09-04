# we might have multiple templates to test, some might be better than others
MESSAGE_TEMPLATE_1 = '''
Generate a snippet of a python function that accomplishes the task '{FUNCTION_TASK}'.
Do not include an inputs or actual code implementation. Only return the snippet.

An example of a snippet is:
    
def example_function(
    num_tickets: int,
    destination: str,
    departure_date: str,
    passengers: List[Dict[str, str]],
) -> Dict[str, float]:
    """
    Orders airplane tickets and returns the total price.
    
    Parameters:
        num_tickets (int): The number of tickets to buy.
        destination (str): The destination city.
        departure_date (str): The departure date in YYYY-MM-DD format.
        passengers (List[Dict[str, str]]): A list of dictionaries containing passenger details.
                                          Each dictionary should have 'name' and 'age' keys.
                                          
    Returns:
        Dict[str, float]: A dictionary with 'total_price' as a key and the total price as a value.
    """
'''
