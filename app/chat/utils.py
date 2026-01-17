from openai import OpenAI
import os
from app.chat.tools import (
    get_cart_for_user,
    add_product_to_cart,
    remove_product_from_cart,
    get_products_for_llm
)
import json

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
def call_chatgpt(messages, tools=None, user_id=None):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    msg = response.choices[0].message

    if msg.tool_calls:
        messages.append(msg)

        for tool_call in msg.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments or "{}")

            if name == "get_cart_for_user":
                result = get_cart_for_user(user_id)

            elif name == "add_product_to_cart":
                result = add_product_to_cart(
                    user_id=user_id,
                    product_id=args.get("product_id")
                )

            elif name == "remove_product_from_cart":
                result = remove_product_from_cart(
                    user_id=user_id,
                    product_id=args.get("product_id")
                )

            elif name == "get_products_for_llm":
                result = get_products_for_llm(
                    limit=args.get("limit", 10)
                )

            else:
                result = "Nieznana akcja."

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result, ensure_ascii=False)
            })

        final_response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages
        )

        return final_response.choices[0].message.content

    return msg.content