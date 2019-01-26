from molinterrogator.target import _target_df
from molinterrogator.target import _compound_df
from molinterrogator.target import _compound_from_target_df

def _target_id_2_card_dict(uniprot_id=None):

        import urllib
        import xmltodict

        url = 'http://www.uniprot.org/uniprot/'+uniprot_id+'.xml'
        request = urllib.request.Request(url)
        request.add_header('User-Agent', 'Python at https://github.com/uibcdf/MolInterrogator || prada.gracia@gmail.com')
        response = urllib.request.urlopen(request)
        xml_result = response.read().decode('utf-8')
        dict_result = xmltodict.parse(xml_result)
        dict_result = dict_result['uniprot']['entry']

        tmp_dict = {}
        tmp_dict['Name'] = dict_result['name']
        tmp_dict['Full Name'] = dict_result['protein']['recommendedName']['fullName']
        if 'shortName' in dict_result['protein']['recommendedName'].keys():
            tmp_dict['Short Name'] = dict_result['protein']['recommendedName']['shortName']
        if 'alternativeName' in dict_result['protein'].keys():
            if type(dict_result['protein']['alternativeName'])==list:
                for alternativeName in dict_result['protein']['alternativeName']:
                    try:
                        tmp_dict['Alternative Name'].append(alternativeName['fullName'])
                    except:
                        tmp_dict['Alternative Name'] = [alternativeName['fullName']]
            else:
                tmp_dict['Alternative Name'] = dict_result['protein']['alternativeName']['fullName']
        tmp_dict['Type'] = 'Protein'
        if 'organism' in dict_result.keys():
            if type(dict_result['organism']['name'])==list:
                for name in dict_result['organism']['name']:
                    if name['@type']=='scientific':
                        tmp_dict['Organism']=name['#text']
            else:
                tmp_dict['Organism'] = dict_result['organism']['name']['#text']
        if 'organismHost' in dict_result.keys():
            tmp_dict['Host'] = dict_result['organismHost']['name'][0]['#text']
        if type(dict_result['comment'])== list:
            for comment in dict_result['comment']:
                if comment['@type']=='function':
                    if type(comment['text'])==list:
                        for function in comment['text']:
                            try:
                                tmp_dict['Function'].append(function['#text'])
                            except:
                                tmp_dict['Function'] = [function['#text']]
                    else:
                        try:
                            tmp_dict['Function'] = comment['text']['#text']
                        except:
                            tmp_dict['Function'] = comment['text']
        else:
            if dict_result['comment']['@type']=='function':
                tmp_dict['Function']=dict_result['comment']['text']

        tmp_dict['UniProt']=dict_result['accession']

        for dbreference in dict_result['dbReference']:
            if dbreference['@type']=='ChEMBL':
                tmp_dict['ChEMBL']=dbreference['@id']
            elif dbreference['@type']=='BioGRID':
                tmp_dict['BioGRID']=dbreference['@id']
            elif dbreference['@type']=='ProteinModelPortal':
                tmp_dict['ProteinModelPortal']=dbreference['@id']
            elif dbreference['@type']=='SMR':
                tmp_dict['Swiss-Model']=dbreference['@id']
            elif dbreference['@type']=='DIP':
                tmp_dict['DIP']=dbreference['@id']
            elif dbreference['@type']=='ELM':
                tmp_dict['ELM']=dbreference['@id']
            elif dbreference['@type']=='IntAct':
                tmp_dict['IntAct']=dbreference['@id']
            elif dbreference['@type']=='MINT':
                tmp_dict['MINT']=dbreference['@id']
            elif dbreference['@type']=='BindingDB':
                tmp_dict['BindingDB']=dbreference['@id']
            elif dbreference['@type']=='InterPro':
                tmp_dict['InterPro']=uniprot_id
            elif dbreference['@type']=='Pfam':
                tmp_dict['Pfam']=dbreference['@id']
            elif dbreference['@type']=='ProDom':
                tmp_dict['ProDom']=dbreference['@id']
            elif dbreference['@type']=='SUPFAM':
                tmp_dict['SUPFAM']=dbreference['@id']
            elif dbreference['@type']=='PDB':
                try:
                    tmp_dict['PDB'].append(dbreference['@id'])
                except:
                    tmp_dict['PDB']=[dbreference['@id']]

        del(url, request, response, urllib, xmltodict, xml_result, dict_result)

        return tmp_dict


class _target_query():

    def __init__(self, query=None):

        self.string = query
        self.query = None
        self.card = _target_df.copy()
        self.compounds = _compound_from_target_df.copy()

        if query is not None:
            self.run_query()
            #self.update_results(index_result=0)

    def run_query(self):

        import urllib

        url = 'http://www.uniprot.org/uniprot/?'

        params = {
            'query':self.string,
            'fil':'reviewed:yes',
            'format':'tab',
            'sort':'score'
        }

        data = urllib.parse.urlencode(params)
        request = urllib.request.Request(url+data)
        request.add_header('User-Agent', 'Python at https://github.com/uibcdf/MolInterrogator || prada.gracia@gmail.com')
        response = urllib.request.urlopen(request)
        self.query=[res.split('\t') for res in response.read().decode('utf-8').split('\n')[1:]]
        self.update_results(index_result=0)

        del(urllib, data, url, request)

    def info_results(self,last=30):

        tmp_df = _target_df.copy()
        ii=0
        for result in self.query:
            uniprot_id = result[0]
            tmp_df =tmp_df.append(_target_id_2_card_dict(uniprot_id),ignore_index=True)
            ii+=1
            if ii==last:
                break

        return tmp_df

    def update_results(self,index_result=0):

        uniprot_id = self.query[index_result][0]
        self.card = _target_df.copy()
        self.card = self.card.append(_target_id_2_card_dict(uniprot_id), ignore_index=True)

        self.compounds = _compound_from_target_df.copy()
        self.interactions = None

