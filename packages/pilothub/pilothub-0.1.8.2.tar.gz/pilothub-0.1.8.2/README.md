---
jupyter:
  kernelspec:
    display_name: base
    language: python
    name: python3
  language_info:
    codemirror_mode:
      name: ipython
      version: 3
    file_extension: .py
    mimetype: text/x-python
    name: python
    nbconvert_exporter: python
    pygments_lexer: ipython3
    version: 3.10.9
  nbformat: 4
  nbformat_minor: 2
---


# Pilothub



to install pilothub use

    pip install pilothub

## PPT Notes Maker

``` python
from pilothub.withopenai import ContentClient
from pilothub.pptnotes import PPTx2Notes

model = "gpt-4-0125-preview"
api_key = "xxxxxxxxxxxxxxxxx"
source_path = r"sample_data.pptx"
dest_path = r"output_file.pptx"
```

``` python
openai_client = ContentClient(openai_api_key=api_key,
                              open_ai_model=model,
                              max_tokens=2500,
                              temperature=0.7)
```

``` python
ppt_client = PPTx2Notes(file_path=source_path)
n = len(ppt_client.slides)
print("Total Number of slides ",n)
```


    Total Number of slides  103



``` python
skip_slides_index = [0,n-3,n-2,n-1,n]
skip_slides_layout = ["1_Custom Layout","Quote Slide","Contemporary_Title v1","Section Header","Last_Slide v1","Quiz","Summary"]
skip_slide_titles = ["quiz","summary"]
ppt_client.set_skip_slides(skip_slides_index=skip_slides_index,
                           skip_slides_layout=skip_slides_layout,
                           skip_slide_titles=skip_slide_titles)
```

``` python
ai_prompt_dict = {
    "CoverPage":"Explain the Module Name in 2 lines",
    "Agenda":"This slide contains the agenda for whole module, provide one line summary for each topic.",
    "Section Header":"This is Section Header, Provide a 5 lines summary on what this section is about.",
    "Quote Slide":"This is a quote slide, provide a 10 lines summary with Key points to remember on what this quote is about.",
    "RunningMan-Infographic":"This is an summary slide, provide a 10 lines summary with Key points to remember on what this infographic is about.",
}

ai_prompt_for_skip_slides = """
You are an expert in course creation, below is text on the slide, provide short notes for this slide in less than 2 lines:

"""
default_prompt = """
            Role: You are an expert in course creation and articulation.
            Task: You need to provide detailed notes, summary & key points.
            Contraints: Keep the notes provided precise and concise.
            Use bullet points to explain the key concepts.
            Do not use any decoration such as bold text (prefer using bullet text)
            Add a section "For Students: " where provide expalanation is
                short format in layman language.(only if necessary/suitable)
            Provide notes for the following information:

            """
ppt_client.write_notes_to_pptx(output_path=dest_path,
                               content_client=openai_client,
                               SET_AI_TEXT_FOR_SKIP_SLIDES=True,
                               AI_PROPMT_SKIP_SLIDES=ai_prompt_for_skip_slides,
                               AI_PROMPT_DICT_SKIP_SLIDES=ai_prompt_dict,
                               DEFAULT_PROMPT_FOR_OTHER_SLIDES=default_prompt,
                               SKIP_NOTES_FOR_SLIDES_WITH_NOTES=True)
```

## PPT to Handbook Maker

``` python
from pilothub.ppt2hb import HandbookMaker



# Set the path of the PowerPoint presentation
ppt_path = r"pilothub.pptx"

# Set the output path for the generated handbook
output_path = "handbook.docx"

# Create an instance of HandbookMaker
handbook_maker = HandbookMaker(ppt_path)


skip_slides = ['Quiz', 'CoverPage', 'RunningMan-Infographic','Last_Slide v1','1_Custom Layout','Contemporary_Title v1']
content_layout_name = "Title and Content"
skip_text_from_slides = ['sample_text1','sample_text2']

# Generate the handbook from the PowerPoint presentation
handbook_maker.convert_ppt_to_handbook(output_file_path=output_path,
                                       skip_slides=skip_slides,
                                       content_layout_name=content_layout_name,
                                       skip_text_from_slides=skip_text_from_slides)
```
