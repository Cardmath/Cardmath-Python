from insights.schemas import OptimalCardsAllocationSolution
import openai
import json

def generate_justification_from_solution(solution: OptimalCardsAllocationSolution) -> str:
    
    prompt = f"""Analyze the following optimal card allocation solution and generate a clear justification for the recommendation.
    The response should explain the key factors that led to this allocation and its benefits.

    Solution details:
    {solution.model_dump_json(indent=3)}

    Generate a plain text justification explaining why this allocation is optimal."""

    response = openai.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that explains credit card allocation strategies. \
             Using the calculation output from an algorithm that computes the optimal allocation of credit card rewards to \
             user's transactions. Please emphasize characteristics of the user's own spending habits when explaining \
             why a card was chosen"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=500
    )
    
    return response.choices[0].message.content.strip()