import os
import sys

TARGET_ENV = 'ci'
env_dir = os.path.join(os.path.dirname(__file__), "..", "environments")

type_name = 'Generic' + sys.argv[1]
ws_type = 'KBaseMatrices.' + sys.argv[1]
spec_txt = open(os.path.dirname(__file__) + '/KBaseMatricesTemplate.yaml').read(
    ).replace('{search_type}', type_name).replace('{WS_type}', ws_type)

with open('{}/{}/types/{}.yaml'.format(env_dir, TARGET_ENV, type_name), 'w') as outfile:
    outfile.write(spec_txt)