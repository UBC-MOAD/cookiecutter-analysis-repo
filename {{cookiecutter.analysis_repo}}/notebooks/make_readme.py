"""Jupyter Notebook collection README generator

Copyright by the UBC EOAS MOAD Group and The University of British Columbia.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

When you add a new notebook to this directory,
rename a notebook,
or change the description of a notebook in its first Markdown cell,
please generate a updated `README.md` file with:

    python3 make_readme.py

and commit and push the updated `README.md` to GitHub.
"""
import datetime
import json
import os
from pathlib import Path
import re


nbviewer = "https://nbviewer.jupyter.org/github"
github_org = "{{ cookiecutter.github_org }}"
repo = "{{ cookiecutter.analysis_repo }}"
url = f"{nbviewer}/{github_org}/{repo}/blob/master/{Path.cwd().name}"

title_pattern = re.compile("#{1,6} ?")
readme = """The Jupyter Notebooks in this directory are made by
{{ cookiecutter.researcher_name }} for sharing of Python code techniques
and notes.

The links below are to static renderings of the notebooks via
[nbviewer.jupyter.org](https://nbviewer.jupyter.org/).
Descriptions below the links are from the first cell of the notebooks
(if that cell contains Markdown or raw text).

"""
for fn in Path(".").glob("*.ipynb"):
    readme += f"* ## [{fn}]({url}/{fn})  \n    \n"
    with open(fn, "rt") as notebook:
        contents = json.load(notebook)
    try:
        first_cell = contents["worksheets"][0]["cells"][0]
    except KeyError:
        first_cell = contents["cells"][0]
    first_cell_type = first_cell["cell_type"]
    if first_cell_type in "markdown raw".split():
        desc_lines = first_cell["source"]
        for line in desc_lines:
            if title_pattern.match(line):
                line = f"{title_pattern.sub('**', line).strip()}**"
            readme += f"    {line}"
        readme += "\n" * 2

license = f"""
## License

These notebooks and files are copyright by the
[UBC EOAS MOAD Group](https://github.com/UBC-MOAD/docs/blob/master/CONTRIBUTORS.rst)
and The University of British Columbia.

They are licensed under the Apache License, Version 2.0.
http://www.apache.org/licenses/LICENSE-2.0
Please see the LICENSE file in this repository for details of the license.
"""

with open("README.md", "wt") as f:
    f.writelines(readme)
    f.writelines(license)
