import jinja2
environment = jinja2.Environment(loader=jinja2.FileSystemLoader("./"))
metaprompt_template = environment.get_template("./templates/metaprompt.jinja")
assistant_template = environment.get_template("./templates/metaprompt_assistant_partial.jinja")
from openai import OpenAI
client = OpenAI()

TASK = input("Describe your task:")
variables = input("What is the variables you want to use (seperate them by comma)?")
VARIABLES = [v.strip() for v in variables.split(",")]

MODEL_NAME = "gpt-4-turbo-preview"
CLIENT = client.chat.completions

prompt = metaprompt_template.render(TASK=TASK)
message = CLIENT.create(
    model=MODEL_NAME,
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content":  prompt
        },
        {
            "role": "assistant",
            "content": assistant_template.render(VARIABLES=VARIABLES)
        }
    ],
    temperature=0
).choices[0].message.content #.content[0].text

from lxml import etree
from jinja2 import meta

def extract_between_tags(input_text:str, tag:str="Instructions", strip: bool = False):
  parser = etree.XMLParser(recover=True)  # recover from bad characters
  tree = etree.fromstring((input_text), parser=parser)
  ext_list = [node.text for node in tree.xpath(f"//{tag}")]
  tag_len = len(f"<{tag}>")
  ext_list = [etree.tostring(node,encoding='unicode')[tag_len:-(tag_len+1)] for node in tree.xpath(f"//{tag}")]
  if strip:
        ext_list = [e.strip() for e in ext_list]
  return ext_list

# TODO
# def remove_empty_tags(text):
#     return re.sub(r'<(\w+)></\1>$', '', text)

def extract_prompt(metaprompt_response):
  between_tags = extract_between_tags(metaprompt_response)[-1].strip()
  return between_tags #remove_empty_tags(remove_empty_tags(between_tags).strip()).strip()


def get_variables(text):
  parsed_content = environment.parse(text)
  return meta.find_undeclared_variables(parsed_content)


extracted_prompt_template = extract_prompt(message)
variables = get_variables(message)

variable_values = {}
for variable in variables:
    print("Enter value for variable:", variable)
    variable_values[variable] = input()

prompt_with_variables = extracted_prompt_template
prompt_with_variables = environment.from_string(prompt_with_variables).render(**variable_values)
print("-"*50)
print(prompt_with_variables)
print("-"*50)

variable_values = {}
for variable in variables:
    print("Enter value for variable:", variable)
    variable_values[variable] = input()

prompt_with_variables = extracted_prompt_template
prompt_with_variables = environment.from_string(prompt_with_variables).render(**variable_values)




message = CLIENT.create(
    model=MODEL_NAME,
    max_tokens=4096,
    response_format = {
    "type": 'json_object',
    },
    messages=[
        {
            "role": "user",
            "content":  prompt_with_variables
        },
    ],
).choices[0].message.content



def cli():
    print("Assistance output on your prompt:\n\n")
    print(message)
