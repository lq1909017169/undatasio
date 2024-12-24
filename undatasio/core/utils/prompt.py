from pydantic import BaseModel

from undatasio.core.utils.fields import Field


class StructuredOutputPrompt(BaseModel):
    extract_prompt: str
    screen_prompt_list: list
    screen_systemctl_prompt: str

    @classmethod
    def create(cls,
               fields: list[Field]
               ) -> BaseModel:
        key_str = "{{"
        for field in fields:
            key_str += (f'"{field.name}": "Extract the value of the key({field.name}) from the article. Return an empty'
                        f' string if the key is not found."')
        key_str += "}}"

        extract_prompt = f"""Given a text passage, please extract specific information and return it in JSON format:
    
        {key_str}
    
        Requirements:
        1. Return results in valid JSON format
        2. Use empty string ("") if information is not found
        3. Only extract relevant information - do not include unrelated context
        4. Keep original phrasing when possible
        5. Remove redundant text that doesn't add meaning
        6. Return only the result data in JSON format.
    
        Example input:
            "NVIDIA reported strong growth in Q3, with revenue reaching $18.1 billion. Jensen Huang, who founded NVIDIA in 
            1993 and serves as CEO, commented that AI demand remains robust. The company expects Q4 revenue to hit $20 billion."
    
        Example output:
        {{
            "third_quarter": "revenue reaching $18.1 billion",
            "founder_ceo": "Jensen Huang",
            "revenue_forecast": "expects Q4 revenue to hit $20 billion"
        }}
    
        Please provide the text passage to analyze."""
        screen_prompt_list = []
        screen_prompt = """You are now a data processing assistant. Please process the data according to the following variables and rules and output it in JSON format:

name: {name}
type: {type}
rule: {rule}

Source text content:
{content}

Processing requirements:
1、Find the information related to {name} in the source text.
2、Extract the corresponding value according to the rule {rule}.
3、Convert the extracted value to the {type} type.
4、Return the result in the specified JSON format.
5、The final output should not include any explanations; only output the resulting JSON data.
"""
        screen_systemctl_prompt = """You are a professional text extraction assistant, specialized in accurately extracting required information from various texts. You must work according to the following principles:

Main Responsibilities:
1. Precise Extraction: Accurately extract required information from source text based on provided rules and patterns
2. Type Conversion: Ensure extracted information matches the required data type
3. Formatted Output: Return results in a unified JSON format

Input Parameters:
- name: The field name to be extracted
- type: Target data type for conversion (supports: string, number, boolean, array, object)
- content: Source text content to be processed
- rule: Extraction rule description

Output Requirements:
1. Must use JSON format for all results
2. Must include both name and value fields
3. The value type must match the specified type requirement

Output Format:
{
    "name": "field_name",
    "value": "extracted_and_converted_value"
}

Important Notes:
1. If required information cannot be extracted from the text, value should return the empty value (corresponding to the data type)
2. If extracted content cannot be converted to the specified type, return the default value for that type
3. Consider possible special characters and formats in the text during extraction
4. Ensure accuracy and consistency of extraction results

Error Handling:
1. Return error message when input parameters are incomplete
2. Request clarification when rules are unclear
3. Explain the reason when type conversion fails

Example:
Input:
name: "price"
type: "number"
content: "Product price: $99.9"
rule: "extract number after 'price:'"

Output:
{
    "name": "price",
    "value": 99.9
}"""
        for f in fields:
            screen_prompt_list.append(
                screen_prompt.format_map({
                    'name': f.name,
                    'type': f.attribute,
                    'rule': f.rule,
                    'content': f.content
                })
            )
        return cls(
            extract_prompt=extract_prompt,
            screen_prompt_list=screen_prompt_list,
            screen_systemctl_prompt=screen_systemctl_prompt
        )
