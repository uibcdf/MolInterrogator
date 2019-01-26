from .target import Target as _Target
from pandas import read_json as pd_read_json

def target(query_string=None):

    return _Target(query_string)

def load(json_file=None):

    import json

    with open(json_file, "r") as read_file:
        interrogatory_json = json.load(read_file)

    if interrogatory_json[0] == '"Target"':
        tmp_target = _Target()
        tmp_target.card = pd_read_json(interrogatory_json[1], orient='table')
        tmp_target._chembl.card = pd_read_json(interrogatory_json[2], orient='table')
        tmp_target._chembl.compounds = pd_read_json(interrogatory_json[3], orient='table')
        tmp_target._uniprot.card = pd_read_json(interrogatory_json[4], orient='table')
        tmp_target._uniprot.compounds = pd_read_json(interrogatory_json[5], orient='table')

    return tmp_target
