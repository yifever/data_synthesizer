MESSAGE_TEMPLATE_1 = """
You are a helpful assistant automating everyday tasks with apis, you are automating {INPUT} related tasks, what are some tasks that you have automated?

Return them in a json format. output should follow this example:
{{
    tasks: [
        {{
            "function_id": "youtube-1",
            "task": "upload a video file as a video to a youtube channel.
        }}, 
        {{
            (next task...)
        }}
    ]
}}

"""
