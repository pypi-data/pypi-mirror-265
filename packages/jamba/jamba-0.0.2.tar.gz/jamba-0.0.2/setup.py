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
    'version': '0.0.2',
    'description': 'jamba - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Jamba\nPyTorch Implementation of Jamba: "Jamba: A Hybrid Transformer-Mamba Language Model"\n\n\n## install\n`$ pip install jamba`\n\n## usage\n\n```python\n# Import the torch library, which provides tools for machine learning\nimport torch\n\n# Import the Jamba model from the jamba.model module\nfrom jamba.model import Jamba\n\n# Create a tensor of random integers between 0 and 100, with shape (1, 100)\n# This simulates a batch of tokens that we will pass through the model\nx = torch.randint(0, 100, (1, 100))\n\n# Initialize the Jamba model with the specified parameters\n# dim: dimensionality of the input data\n# depth: number of layers in the model\n# num_tokens: number of unique tokens in the input data\n# d_state: dimensionality of the hidden state in the model\n# d_conv: dimensionality of the convolutional layers in the model\n# heads: number of attention heads in the model\n# num_experts: number of expert networks in the model\n# num_experts_per_token: number of experts used for each token in the input data\nmodel = Jamba(\n    dim=512,\n    depth=6,\n    num_tokens=100,\n    d_state=256,\n    d_conv=128,\n    heads=8,\n    num_experts=8,\n    num_experts_per_token=2,\n)\n\n# Perform a forward pass through the model with the input data\n# This will return the model\'s predictions for each token in the input data\noutput = model(x)\n\n# Print the model\'s predictions\nprint(output)\n\n```\n\n# License\nMIT\n',
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
