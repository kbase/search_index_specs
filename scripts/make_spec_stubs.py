import os
import sys

env_dir = os.path.join(os.path.dirname(__file__), "..", "environments")


def stub_txt(ws_type):
    return """global-object-type: {}
storage-type: WS
storage-object-type: {}
versions:
  - indexing-rules: []""".format(ws_type.split('.')[-1], ws_type)


def make_stubs(types, env='ci'):
    for ws_type in types:
        file_path = os.path.join(env_dir, env, "types", "{}.yaml".format(ws_type.split('.')[-1]))
        if os.path.exists(file_path):
            continue
        with open(file_path, 'w') as stub:
            stub.write(stub_txt(ws_type))


if __name__ == '__main__':
    make_stubs(sys.argv[1].split(","))
