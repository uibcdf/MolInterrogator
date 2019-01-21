class Target(query_string=None):

    from chembl_webresource_client.new_client import new_client

    tmp_target = Target()

    tmp_target._query_string        = query_string
    tmp_target._chembl_target_query = new_client.target.filter(target_synonym__icontains=target_query_string)
    tmp_target.


