
_engines_name=['ChEMBL']

class Target():

    def __init__(self,query=None,verbose=True):

        self._query_string = query
        self._chembl = _target_chembl_query(query)

        if len(self._chembl._query) > 1:
           print('ChEMBL with', len(self._chembl._query),'targets matching the query. (See xxx to solve it)')

    def info_results(self,engine=None,verbose=True):

        results_list={
            'ChEMBL': self._chembl._info_results()
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

class _target_chembl_query():

    def __init__(self, query=None):

        from chembl_webresource_client.new_client import new_client

        self.query_string = query
        self._query = new_client.target.filter(target_synonym__icontains=self.query_string)
        self._update_results(index_result=0)

    def _info_results(self):

        from pandas import DataFrame as _pd_DataFrame

        df = _pd_DataFrame(columns=['Name','Type','ChemBL_id'])
        for result in self._query:
            tmp_dict = {
                'Name': result['pref_name'],
                'Type': result['target_type'],
                'ChemBL_id': result['target_chembl_id']
            }
            df = df.append(tmp_dict,ignore_index=True)

        return df

    def _update_results(self,index_result=0):

        from chembl_webresource_client.new_client import new_client
        self.target_chembl_id = self._query[index_result]['target_chembl_id']
        self._activity_filter = new_client.molecule.filter(target_chembl_id__in=self.target_chembl_id)
        self._molecule_filter = new_client.activity.filter(target_chembl_id__in=self.target_chembl_id)
        self.compounds_chembl_id = None

