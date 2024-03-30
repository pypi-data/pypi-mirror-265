def org(text, openai_key, model='gpt-3.5-turbo', save=False):
  """
  Perform Named Entity Recognition (NER), specifically of organizations.

  Args:
    text (str): Text to be analyzed.
    openai_key (str): OpenAI API key.
    model (str, optional): Model to be used for the analysis. Defaults to 'gpt-3.5-turbo'.
    save (bool, optional): If True, the output will be saved as an Excel file. Defaults to False.

  Returns:
    pandas.DataFrame: DataFrame containing the extracted organizations.
  """

  from openai import OpenAI
  import os
  import json
  import pandas as pd

  os.environ['OPENAI_API_KEY'] = openai_key
  client = OpenAI()

  prompt = f"""
  I will provide a text from which you must extract the names of organizations. You must follow the following rules:
  - Do not extract names from geographic locations (such as countries, states, or cities). Organization names only.
  - If an organization's name is followed by its acronym in brackets, extract only the full name, excluding the acronym from the output.
  - Please present the output strictly as a Python list, showing only the list and nothing else.
  - If there is no organizatons in the text, the output must be an empty Python list.
  Here is the text:
  {text}
  """

  response = client.chat.completions.create(
      model=model,
      messages=[
        {"role": "system", "content": "You are a helpful assistant, specialized in extracting names of organizations of a text."},
        {"role": "user", "content": prompt}
      ],
      temperature=0.0,
      max_tokens=1000,
      top_p=0.0,
      frequency_penalty=0.0,
      presence_penalty=0.0,
      stop=None
    )

  response_dict = json.loads(response.json())
  content = response_dict['choices'][0]['message']['content']

  start_index = content.find('[')
  end_index = content.find(']') + 1
  content_list = content[start_index:end_index]

  org_list = eval(content_list)

  df = pd.DataFrame(org_list, columns=["Organizations"])

  if save==True:
    df.to_excel('organizations.xlsx', index=False)

  return df
