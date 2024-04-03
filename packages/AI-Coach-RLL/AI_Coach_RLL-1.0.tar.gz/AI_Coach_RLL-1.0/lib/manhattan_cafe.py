import openai

class AI_Coach_RLL:
    def get_completion(prompt, model="gpt-4-turbo-preview"):
        messages = [{"role": "user", "content": prompt}]
        from openai import OpenAI
        
        client=OpenAI(api_key=openai.api_key)
        response=client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.2,
        )
        response_message = response.choices[0].message.content
        return response_message