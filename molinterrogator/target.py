from pandas import DataFrame as _pd_DataFrame

_engines_name=['ChEMBL','UniProt']

_target_df   = _pd_DataFrame( columns=['Name', 'Type', 'Organism', 'ChemBL', 'UniProt', 'BindingDB', 'IntAct',
                                       'InterPro', 'PDB'])
_compound_df = _pd_DataFrame(columns=[])
_compound_from_target_df   = _pd_DataFrame(columns=['Name', 'Smile', 'Compound ChemBL', 'Assay ChemBL',
                                      'Document ChemBL','IC50'])

class Target():

    def __init__(self,query=None,verbose=True):

        self._query_string = query
        self._chembl = _target_chembl_query(query)
        self._uniprot = _target_uniprot_query(query)
        self.card = _target_df.copy()

        if len(self._chembl.query) > 1:
           print('ChEMBL with', len(self._chembl.query),'targets matching the query. (See xxx to solve it)')

    def info_results(self,engine=None,verbose=True):

        results_list={
            'ChEMBL': self._chembl.info_results()
        }

        if engine is None:
            if verbose:
                for database in results_list.keys():
                    print(database,'with',len(results_list[database]),'targets matching the query.')
            else:
                return results_list
        else:
            return results_list[engine]

    def update_results(self,engine=None,index_result=None):

        if engine=='ChEMBL':
            self._chembl._update_results(index_result)

        pass

def _target_chembl_id_2_card_dict(chembl_id=None, client=None):

        result = client.target.filter(target_chembl_id__in=chembl_id)[0]
        tmp_dict = {}
        tmp_dict['Name'] = result['pref_name']
        tmp_dict['Type'] = result['target_type']
        tmp_dict['Organism'] = result['organism']
        tmp_dict['ChemBL'] = result['target_chembl_id']
        if len(result['target_components'])>1:
            print('El target ',tmp_dict['ChemBL'],'tiene más de un target_components y no se que\
                  es.')
        for xref in result['target_components'][0]['target_component_xrefs']:
            src_db = xref['xref_src_db']
            id_db = xref['xref_id']
            if src_db == 'PDBe':
                try:
                    tmp_dict['PDB'].append(id_db)
                except:
                    tmp_dict['PDB']=[id_db]
            elif src_db == 'UniProt':
                try:
                    tmp_dict['UniProt'].append(id_db)
                except:
                    tmp_dict['UniProt']=[id_db]
            elif src_db == 'IntAct':
                try:
                    tmp_dict['IntAct'].append(id_db)
                except:
                    tmp_dict['IntAct']=[id_db]
            elif src_db == 'InterPro':
                try:
                    tmp_dict['InterPro'].append(id_db)
                except:
                    tmp_dict['InterPro']=[id_db]

        tmp_dict['BindingDB']=tmp_dict['UniProt']

        del(result)

        return tmp_dict

def _compound_from_target_chembl_2_card_dict(compound_result=None, client=None):

        tmp_dict = {}
        tmp_dict['Name'] = compound_result['molecule_pref_name']
        tmp_dict['Smile'] = compound_result['canonical_smiles']
        tmp_dict['Compound ChemBL'] = compound_result['molecule_chembl_id']
        tmp_dict['Assay ChemBL'] = compound_result['assay_chembl_id']
        tmp_dict['Document ChemBL'] = compound_result['document_chembl_id']

        if compound_result['standard_type']=='IC50':
            tmp_dict['IC50']=compound_result['standard_value']+' '+compound_result['standard_units']
        else:
            print('Type of compound value not known for molecule_chembl_id:', compound_result['molecule_chembl_id'])

        return tmp_dict

class _target_uniprot_query():

    def __init__(self, query=None):

        self.string = query
        self.query = None
        self.card = _target_df.copy()

        self.run_query()
        #self.update_results(index_result=0)

    def run_query(self):

        import urllib

        url = 'http://www.uniprot.org/uniprot/'

        params = {
            'query':self.string,
            'reviewed':'yes',
            'format':'tab',
            'sort':'score'
        }

        data = urllib.parse.urlencode(params)
        request = urllib.request.Request(url, data)
        print(request)
        response = urllib.request.urlopen(request)

        self.query = response

        del(urllib, urllib2, data, url, request)

class _target_chembl_query():

    def __init__(self, query=None):

        self.string = query
        self.query = None
        self.card = _target_df.copy()

        self.run_query()
        self.update_results(index_result=0)

    def run_query(self):

        from chembl_webresource_client.new_client import new_client
        self.query = new_client.target.filter(target_synonym__icontains=self.string)
        del(new_client)

    def info_results(self):

        from chembl_webresource_client.new_client import new_client

        tmp_df = _target_df.copy()
        for result in self.query:
            chembl_id = result['target_chembl_id']
            tmp_df =tmp_df.append(_target_chembl_id_2_card_dict(chembl_id, new_client),ignore_index=True)

        del(new_client)

        return tmp_df

    def update_results(self,index_result=0):

        from chembl_webresource_client.new_client import new_client

        chembl_id = self.query[index_result]['target_chembl_id']

        self.card = _target_df.copy()
        self.card =self.card.append(_target_chembl_id_2_card_dict(chembl_id, new_client),ignore_index=True)

        self.activity_filter = new_client.molecule.filter(target_chembl_id__in=chembl_id)
        self.molecule_filter = new_client.activity.filter(target_chembl_id__in=chembl_id)

        self.compounds = _compound_from_target_df.copy()

        for result in self.molecule_filter:
            tmp_dict = _compound_from_target_chembl_2_card_dict(result, new_client)
            self.compounds = self.compounds.append(tmp_dict,ignore_index=True)
