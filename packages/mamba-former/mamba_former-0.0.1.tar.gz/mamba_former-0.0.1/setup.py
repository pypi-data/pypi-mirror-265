# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mamba_former']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'swarms', 'torch', 'zetascale']

setup_kwargs = {
    'name': 'mamba-former',
    'version': '0.0.1',
    'description': 'Paper - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# MambaFormer\nImplementation of MambaFormer in Pytorch ++ Zeta from the paper: "Can Mamba Learn How to Learn? A Comparative Study on In-Context Learning Tasks"\n\n## install\n`pip3 install mamba-former`\n\n## usage\n```python\nimport torch \nfrom mamba_former.main import MambaFormer\n\n# Forward pass example\nx = torch.randint(1, 1000, (1, 100)) # Token\n# Tokens are integrers\n\n# Model\nmodel = MambaFormer(\n    dim = 512,\n    num_tokens = 1000,\n    depth = 6,\n    d_state = 512,\n    d_conv = 128,\n    heads = 8,\n    dim_head = 64,\n    return_tokens = True\n)\n\n# Forward\nout = model(x)\nprint(out)\nprint(out.shape)\n```\n\n\n# License\nMIT\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/MambaFormer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
