CHAT_TEMPLATE = \
'''
<s>[INST] <<SYS>>
{SYSTEM_MESSAGE}
<</SYS>>

{CONVERSATION}'''

EXCHANGE_TEMPLATE = \
'''
{USER_MESSAGE} [/INST] {MODEL_REPLY}</s><s>[INST] '''
# {user_message_2} [/INST] , etc...
# the space at the end of this string is INTENTIONAL

LATEST_USER_TEMPLATE = \
'''{USER_MESSAGE_LATEST} [/INST]'''

SYSTEM_MESSAGE_TEMPLATE = \
'''
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

You have access to the following functions, described in json.
{FUNCTION_DESCRIPTIONS}

If calling the functions are useful, you may call them with a "function_call" json reponse. If you don't have the required parameters for a function call, ask the user to clarify and provide you the requirements. 
'''

