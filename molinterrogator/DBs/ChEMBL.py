from molinterrogator.target import _target_df
from molinterrogator.target import _compound_df
from molinterrogator.target import _compound_from_target_df

def _target_id_2_card_dict(db_id=None, client=None):

        result = client.target.filter(target_chembl_id__in=db_id)[0]
        tmp_dict = {}
        tmp_dict['Name'] = result['pref_name']
        tmp_dict['Type'] = result['target_type']
        tmp_dict['Organism'] = result['organism']
        tmp_dict['ChEMBL'] = result['target_chembl_id']
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
            elif src_db == 'Pfam':
                try:
                    tmp_dict['Pfam'].append(id_db)
                except:
                    tmp_dict['Pfam']=[id_db]

        tmp_dict['BindingDB']=tmp_dict['UniProt']

        del(result)

        return tmp_dict

def _compound_from_target_2_card_dict(from_target_result=None, client=None):

        db_id = from_target_result['molecule_chembl_id']

        tmp_dict = {}

        molecule_result = client.molecule.filter(molecule_chembl_id__in=db_id)[0]
        tmp_dict['Name'] = molecule_result['pref_name']
        for ii in molecule_result['molecule_synonyms']:
            if ii['syn_type']=='FDA':
                tmp_dict['FDA Name']=ii['molecule_synonym']
            elif ii['syn_type']=='TRADE NAME':
                tmp_dict['Trade Name']=ii['molecule_synonym']
            else:
                try:
                    tmp_dict['Alternative Name'].append(ii['molecule_synonym'])
                except:
                    tmp_dict['Alternative Name']=[ii['molecule_synonym']]

        tmp_dict['Natural']=molecule_result['natural_product']

        tmp_dict['Smile'] = molecule_result['molecule_structures']['canonical_smiles']
        tmp_dict['InChi'] = molecule_result['molecule_structures']['standard_inchi']
        tmp_dict['InChi Key'] = molecule_result['molecule_structures']['standard_inchi_key']
        tmp_dict['ChemBL'] = molecule_result['molecule_chembl_id']
        tmp_dict['Max Phase'] = molecule_result['max_phase']
        tmp_dict['Type'] = molecule_result['molecule_type']
        tmp_dict['Chirality'] = molecule_result['chirality']
        tmp_dict['ACD LogD'] = molecule_result['molecule_properties']['acd_logd']
        tmp_dict['ACD LogP'] = molecule_result['molecule_properties']['acd_logP']
        tmp_dict['ACD Acidic pKa'] = molecule_result['molecule_properties']['acd_most_apka']
        tmp_dict['ACD Basic pKa'] = molecule_result['molecule_properties']['acd_most_bpka']
        tmp_dict['ALogP'] = molecule_result['molecule_properties']['alogp']
        tmp_dict['Aromatic Rings'] = molecule_result['molecule_properties']['aromatic_rings']
        tmp_dict['Molecular Formula'] = molecule_result['molecule_properties']['full_molformula']
        tmp_dict['Molecular Weight'] = molecule_result['molecule_properties']['full_mwt']
        tmp_dict['HBA'] = molecule_result['molecule_properties']['hba']
        tmp_dict['HBD'] = molecule_result['molecule_properties']['hbd']
        tmp_dict['HBA (Lipinski)'] = molecule_result['molecule_properties']['hba_lipinski']
        tmp_dict['HBD (Lipinski)'] = molecule_result['molecule_properties']['hbd_lipinski']
        tmp_dict['Heavy Atoms'] = molecule_result['molecule_properties']['heavy_atoms']
        tmp_dict['Molecular Species'] = molecule_result['molecule_properties']['molecular_species']
        tmp_dict['Molecular Weight Monoisotopic'] =molecule_result['molecule_properties']['mw_monoisotopic']
        tmp_dict['Rule of 5 Violations']=molecule_result['molecule_properties']['num_ro5_violations']
        tmp_dict['Rule of 5 Violations (Lipinski)']=molecule_result['molecule_properties']['num_lipinski_ro5_violations']
        tmp_dict['Polar Surface Area']=molecule_result['molecule_properties']['psa']
        tmp_dict['QED Weighted']=molecule_result['molecule_properties']['qed_weighted']
        tmp_dict['Rotatable Bonds']=molecule_result['molecule_properties']['rtb']

        import urllib
        url = 'https://www.ebi.ac.uk/unichem/rest/verbose_inchikey/'+tmp_dict['InChi Key']
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        unichem_result = eval(response.read())
        for ii in unichem_result:
            if ii['name']=='drugbank':
                tmp_dict['DrugBank']=ii['src_compound_id']
            if ii['name']=='gtpdb':
                tmp_dict['Guide to Pharmacology']=ii['src_compound_id']
            if ii['name']=='zinc':
                tmp_dict['ZINC']=ii['src_compound_id']
            if ii['name']=='surechembl':
                tmp_dict['SureChEMBL']=ii['src_compound_id']
            if ii['name']=='surechembl':
                tmp_dict['SureChEMBL']=ii['src_compound_id']
            if ii['name']=='pubchem_tpharma':
                tmp_dict['PubChem Thomson Pharma']=ii['src_compound_id']
            if ii['name']=='pubchem':
                tmp_dict['PubChem']=ii['src_compound_id']
            if ii['name']=='lincs':
                tmp_dict['LINCS']=ii['src_compound_id']
            if ii['name']=='nikkaji':
                tmp_dict['Nikkaji']=ii['src_compound_id']
            if ii['name']=='bindingdb':
                tmp_dict['BindingDB']=ii['src_compound_id']
            if ii['name']=='comptox':
                tmp_dict['EPA Comptox']=ii['src_compound_id']
            if ii['name']=='drugcentral':
                tmp_dict['Drug Central']=ii['src_compound_id']

        del(urllib, request, response, unichem_result)

        tmp_dict['Compound ChemBL'] = molecule_result['molecule_chembl_id']
        tmp_dict['Assay ChemBL'] = compound_result['assay_chembl_id']
        tmp_dict['Document ChemBL'] = compound_result['document_chembl_id']

        if compound_result['standard_type']=='IC50':
            tmp_dict['IC50']=compound_result['standard_value']+' '+compound_result['standard_units']
        else:
            print('Type of compound value not known for molecule_chembl_id:', compound_result['molecule_chembl_id'])

        return tmp_dict

class _target_query():

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
            tmp_df =tmp_df.append(_target_id_2_card_dict(chembl_id, new_client),ignore_index=True)

        del(new_client)

        return tmp_df

    def update_results(self,index_result=0):

        from chembl_webresource_client.new_client import new_client

        chembl_id = self.query[index_result]['target_chembl_id']

        self.card = _target_df.copy()
        self.card =self.card.append(_target_id_2_card_dict(chembl_id, new_client),ignore_index=True)

        self.activity_filter = new_client.molecule.filter(target_chembl_id__in=chembl_id)
        self.molecule_filter = new_client.activity.filter(target_chembl_id__in=chembl_id)

        self.compounds = _compound_from_target_df.copy()

        for result in self.molecule_filter:
            tmp_dict = _compound_from_target_2_card_dict(result, new_client)
            self.compounds = self.compounds.append(tmp_dict,ignore_index=True)

