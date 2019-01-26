import nbformat as nbf


class Target_Notebook():

    def __init__(self, interrogatory=None, json_file=None):

        ii=interrogatory

        self.Title = """\
# {}
""".format(ii._chembl.card["Name"][0])

        self.Function = """\
## Function
{}
""".format(ii._uniprot.card['Function'][0])

        self.Sequence = """\
## Sequence
"""

        self.Structure = """\
## Structure
"""

        self.Models = """\
## Structure
"""

        self.code = """\
import molinterrogator as mi
target = mi.load('{}')
""".format(json_file)


        self.structure = [
            ["Title", "text"],
            ["Function", "text"],
            ["Sequence", "text"],
            ["Models", "text"],
            ["code", "code"]
        ]

def make_Notebook(interrogatory=None, output='target.ipynb',json_file=None):

    import nbformat as nbf
    from nbconvert.preprocessors import ExecutePreprocessor

    if interrogatory.type == 'Target':
        content = Target_Notebook(interrogatory,json_file)
    else:
        print('Not implemented yet.')

    nb = nbf.v4.new_notebook()

    nb['cells'] = []

    for item in content.structure:
        cell_content = content.__getattribute__(item[0])
        if item[1]=='text':
            cell = nbf.v4.new_markdown_cell(cell_content)
        elif item[1]=='code':
            cell = nbf.v4.new_code_cell(cell_content)
        nb['cells'].append(cell)

    #jupyter nbconvert --execute --inplace test.ipynb

    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(nb, {'metadata': {'path': '.'}})

    with open(output, 'wt') as f:
        nbf.write(nb, f)

    pass

