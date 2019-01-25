from pandas import DataFrame as _pd_DataFrame

_target_df   = _pd_DataFrame( columns=['Name', 'Full Name', 'Short Name', 'Alternative Name', 'Type', 'Organism',
                                       'Host', 'Function', 'ChEMBL', 'UniProt', 'BindingDB', 'IntAct',
                                       'BioGRID', 'ProteinModelPortal', 'Swiss-Model',
                                       'DIP', 'ELM', 'MINT', 'PDB', 'InterPro', 'Pfam', 'ProDom',
                                       'SUPFAM', 'Mutagenesis'])

_compound_df = _pd_DataFrame(columns=['Name',
                                      'Alternative Name',
                                      'FDA Name',
                                      'FDA UNII',
                                      'Trade Name',
                                      'PubChem',
                                      'Type',
                                      'Max Phase',
                                      'Smile',
                                      'InChi',
                                      'InChi Key',
                                      'ChEMBL',
                                      'DrugBank',
                                      'Guide to Pharmacology',
                                      'ZINC',
                                      'SureChEMBL',
                                      'PubChem Thomson Pharma',
                                      'LINCS',
                                      'Nikkaji',
                                      'BindingDB',
                                      'EPA Comptox',
                                      'Drug Central',
                                      'Molecular Formula',
                                      'Natural',
                                      'Chirality',
                                      'ACD LogP',
                                      'ACD LogD',
                                      'ACD Acidic pKa',
                                      'ACD Basic pKa',
                                      'ALogP',
                                      'Aromatic Rings',
                                      'Molecular Weight',
                                      'HBA',
                                      'HBD',
                                      'HBA (Lipinski)',
                                      'HBD (Lipinski)',
                                      'Heavy Atoms',
                                      'Molecular Species',
                                      'Molecular Weight Monoisotopic',
                                      'Rule of 5 Violations',
                                      'Rule of 5 Violations (Lipinski)',
                                      'Polar Surface Area',
                                      'QED Weighted',
                                      'Rotatable Bonds'
                                     ])

_compound_from_target_df = _pd_DataFrame(columns=list(_compound_df.columns)+['Assay ChEMBL', 'Document ChEMBL', 'IC50'])

_dbs_multi=['ChEMBL','UniProt']
_dbs_models=['ProteinModelPortal', 'Swiss-Model']
_dbs_interactions=['IntAct', 'BioGRID', 'DIP', 'ELM', 'MINT']
_dbs_compounds=['BindingDB']
_dbs_structure=['PDB']
_dbs_mutagenesis=[]
_dbs_posttrans_mod=[]
_dbs_domains=['InterPro', 'Pfam', 'ProDom', 'SUPFAM']
_dbs_similarities=[]
_dbs_regions=[]

# PDB, PDBe, CREDO, PDBsuf

# Binding Sites or Poses
# Clefts, pores, pockets, ...

class Target():

    def __init__(self,query=None,verbose=True):

        from .DBs.ChEMBL import _target_query as _target_chembl_query
        from .DBs.UniProt import _target_query as _target_uniprot_query
        from .DBs.BindingDB import _target_query as _target_bindingdb_query

        self._query_string = query
        self._chembl = None
        self._uniprot = None
        self._bindingdb = None

        # DBs Multi
        ## ChEMBL
        self._chembl = _target_chembl_query(query)
        ## UniProt
        self._uniprot = _target_uniprot_query(query)

        # DBs Compounds
        ## BindingDB
        #bindingdb_ids=[target._chembl.card['BindingDB'].tolist(),target._uniprot.card['BindingDB'].tolist()]
        #ids=[]
        #for ii in bindingdb_ids:
        #    if type(ii)==list:
        #        for jj in ii:
        #            if type(jj)==list:
        #                for kk in jj:
        #                    ids.append(kk)
        #            else:
        #                ids.append(jj)
        #    else:
        #        ids.append(ii)
        #binding_ids=list(set(ids))
        #self._bindingdb = _target_bindingdb_query(binding_ids)

        # DBs Models

        self.card = _target_df.copy()

        if verbose:
            if len(self._chembl.query) > 1:
                print('ChEMBL with', len(self._chembl.query),'targets matching the query. (See xxx to \
                    refine the result)')
            if len(self._uniprot.query) > 1:
                print('UniProt with', len(self._uniprot.query),'targets matching the query. (See xxx to \
                    refine the result)')

    def info_results(self,engine=None,verbose=True):

        results_list={
            'ChEMBL': self._chembl.info_results(),
            'UniProt': self._uniprot.info_results()
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


