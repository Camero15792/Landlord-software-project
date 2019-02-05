import math, os, json
from pathlib import Path
import jsonpickle

FILE = 'test.dat'


class Store:
    def __init__(self):
        pass


    def write_chain(self, tenant_chain):
        with open(str(Path(os.path.dirname(os.path.realpath(__file__)), FILE)), 'w') as file:
            for tenant in tenant_chain:
                obj_json = jsonpickle.dumps(tenant)
                file.write(obj_json +'\n')


    def read_chain(self):

        tenant_chain = []

        with open(str(Path(os.path.dirname(os.path.realpath(__file__)), FILE))) as file:

            for line in file.readlines():
                tenant_chain.append(jsonpickle.loads(line))

        return tenant_chain



if __name__ == "__main__":

    from tenant_data import Tenant

    # Lets get the basic information into our object. prorated is automatically generated.
    example_tenant = Tenant(400, '05/15/19', '05/15/20')

    # If we want to reference this tenant we can read its unique ID, later on we can reference using the tenants name once we know it.
    print(id(example_tenant))

    # The tenant gave us his drivers licesnse so now we can add his legal name to the object
    example_tenant.first_name = 'John'
    example_tenant.last_name = 'Doe'

    # We can great a list with an arbitrary amount of tenants
    all_tenants = [example_tenant, Tenant(600, '02/15/19', '02/15/21')]

    # ...and keep their unique IDs from each other even though we dont know the name of tenant 2
    print(id(all_tenants[0]))
    print(id(all_tenants[1]))

    store = Store()
    store.write_chain(all_tenants)
    obj_chain = store.read_chain()

    print(obj_chain)
