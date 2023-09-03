
import openai
import config
openai.api_key = config.OPENAI_API_KEY


def extract_unavailable_shifts_from_text(employee_id, text) -> list[dict]:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {
                "role": "system",
                "content": "you will get a message from an employee with an employee id telling you which shifts he can or cannot work\nyou need to know that morning shift are shift_id 1\nafternoon shifts are 2\nnight shifts are 3\nyou need to parse from it a list of json in a pattern like this:\n[\n  {\n    \"date\": \"2023-01-01\",\n    \"shift_type_id\": 1\n  },\n  {\n    \"date\": \"2023-01-01\",\n    \"shift_type_id\": 2\n  }\n]"
            },
            {"role": "user", "content": f"employee_id: {employee_id} message: {text}"},
        ],
        temperature=0.5,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response.choices[0].message.content