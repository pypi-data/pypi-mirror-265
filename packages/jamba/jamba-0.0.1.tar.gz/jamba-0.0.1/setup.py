# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jamba']

package_data = \
{'': ['*']}

install_requires = \
['swarms', 'torch', 'zetascale']

setup_kwargs = {
    'name': 'jamba',
    'version': '0.0.1',
    'description': 'jamba - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Jamba\nPyTorch Implementation of Jamba: "Jamba: A Hybrid Transformer-Mamba Language Model"\n\n\n## install\n`$ pip install jamba`\n\n## usage\n\n```\nimport torch \nfrom jamba.model import JambaBlock\n\n# Create a random tensor of shape (1, 128, 512)\nx = torch.randn(1, 128, 512)\n\n# Create an instance of the JambaBlock class\njamba = JambaBlock(\n    512,  # input channels\n    128,  # hidden channels\n    128,  # key channels\n    8,    # number of heads\n    4,    # number of layers\n)\n\n# Pass the input tensor through the JambaBlock\noutput = jamba(x)\n\n# Print the shape of the output tensor\nprint(output.shape)\n```\n\n# License\nMIT\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/jamba',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
