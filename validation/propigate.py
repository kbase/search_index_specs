import os
from distutils.dir_util import copy_tree

SOURCE_ENV = 'ci'
TARGET_ENVS = ('appdev', 'next', 'prod')
env_dir = os.path.join(os.path.dirname(__file__), "..", "environments")

for target in TARGET_ENVS:
    copy_tree(os.path.join(env_dir, SOURCE_ENV, 'types/'), os.path.join(env_dir, target, 'types/'))
