# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gamba_torch']

package_data = \
{'': ['*']}

install_requires = \
['swarms', 'torch', 'zetascale']

setup_kwargs = {
    'name': 'gamba-torch',
    'version': '0.0.1',
    'description': 'gamba - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Gamba\nImplementation of "GAMBA: MARRY GAUSSIAN SPLATTING WITH MAMBA FOR SINGLE-VIEW 3D RECONSTRUCTION" in PyToch\n\n## install\n`$ pip intall gamba`\n\n## usage\n```python\nimport torch \nfrom gamba.main import Gamba\n\n\n# Forward pass of the GambaDecoder module.\nx = torch.randn(1, 1000, 512)\n\n# Model\nmodel = Gamba(\n    dim=512,\n    d_state=512,\n    d_conv=512,\n    n=16384,\n    depth=3\n)\n\n# Out\nout = model(x)\nprint(out)\n```\n\n\n# License\nMIT\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/gamba',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
