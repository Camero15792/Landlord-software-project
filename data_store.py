import os, json
from pathlib import Path



class JSON:
    def __init__(self, json_file):
        self.json_file = json_file


    def write_chain(self, tenant_chain):

        processed_list = []

        for tenant in tenant_chain:
            processed_list.append(tenant.__dict__)

        with open(str(Path(os.path.dirname(os.path.realpath(__file__)), self.json_file)), 'w') as file:
            json.dump(processed_list, file, indent=4, default=obj_encode)


    def read_chain(self):

        with open(str(Path(os.path.dirname(os.path.realpath(__file__)), self.json_file))) as file:
            tenant_chain = json.load(file, object_hook=obj_decode)

        return tenant_chain



def obj_encode(obj):
    if type(obj) is datetime.datetime:
        obj = obj.strftime('%x')

    return obj


def obj_decode(chain_dict):
    for key, value in chain_dict.items():
        try:
            chain_dict[key] = datetime.datetime.strptime(value, '%x')
        except Exception as Msg:
            pass

    return chain_dict



if __name__ == "__main__":

    from tenant_data import Tenant
    import datetime

    current_dir = os.path.dirname(os.path.realpath(__file__))

    tenant1 = Tenant()
    tenant1.lease_start_date = datetime.datetime.now()
    tenant1.lease_end_date = datetime.datetime.now()
    tenant1.rent_per_month = 400
    tenant1.rent_prorated = 207
    tenant1.first_name = "John"
    tenant1.last_name = 'Doe'
    tenant1.utility_share_portion = 0.3
    tenant1.tenant_address = "123 easy street, colorado springs, CO 80923"
    tenant1.tenant_unit = "A"
    tenant1.tenant_id = 1549674307163

    tenant_chain = []
    tenant_chain.append(tenant1)

    tenant2 = Tenant()
    tenant2.lease_start_date = datetime.datetime.now()
    tenant2.lease_end_date = datetime.datetime.now()
    tenant2.rent_per_month = 400
    tenant2.rent_prorated = 207
    tenant2.first_name = "John"
    tenant2.last_name = 'Doe'
    tenant2.utility_share_portion = 0.3
    tenant2.tenant_address = "123 easy street, colorado springs, CO 80923"
    tenant2.tenant_unit = "A"
    tenant2.tenant_id = 1549674307163

    tenant_chain.append(tenant1)

    JSON(os.path.join(current_dir, 'TenantInfo.dat')).write_chain(tenant_chain)


    test_obj = JSON(os.path.join(current_dir, 'TenantInfo.dat')).read_chain()

    print(test_obj)



