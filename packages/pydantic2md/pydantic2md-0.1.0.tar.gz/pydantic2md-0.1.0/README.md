# Pydantic2md


Utility package to translate Pydantic models to markdown.

Useful for logging models in a [Gradio](https://www.gradio.app/)/[Streamlit](https://streamlit.io/) app or simply to generate reports.

It supports most common types, contributions are welcome!

## Usage

```python
from pydantic2md import pydantic2md

class Hero(BaseModel):
    name: str
    age: int

my_hero = Hero(name="Arthur", age=23)

print(pydantic2md(my_hero))

"""
# Hero
 
name (str): Arthur
age (int): 23
"""
```


## Roadmap

- [ ] Live Demo
- [ ] Support light tables