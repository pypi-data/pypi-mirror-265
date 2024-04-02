# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['manamodeller']

package_data = \
{'': ['*']}

install_requires = \
['dexom-python>=1.0',
 'jproperties>=2.1.1',
 'jupyterlab>=4.0',
 'networkx>=2.8.4',
 'numpy>=1.2.0,<2.0.0',
 'pandas<=1.5.0',
 'progressbar>=2.5,<3.0',
 'pyvis>=0.3.2',
 'tqdm>=4.65.0,<5.0.0',
 'xlsxwriter>=3.1.0']

setup_kwargs = {
    'name': 'manamodeller',
    'version': '0.1.0',
    'description': '',
    'long_description': '# MANA\nMANA: mMoA identification Assisted by modelling and Network Analysis.\n\nThis repository contains code and a test case associated with the article named : \n\n    A strategy to detect metabolic changes induced by exposure to chemicals from large sets of condition-specific metabolic models computed with enumeration techniques\n\nThe workflow presented in this article aims at improving our understanding of the metabolic Mechanism of Action and can be divided in three steps:\n1. Condition-specific metabolic network modelling with partial enumeration from gene expression data\n2. Identify Differentially Activated Reactions (DAR) from the modelised sets of condition-specific metabolic networks\n3. Network anaylsis to extract minimal subnetworks représentative of the chemical\'s mMoA\n\nEach step of the workflow is performed by a jupyter notebook:\n* **partial_enumeration.ipynb**\n* **dars_calculation.ipynb**\n* **analysis.ipynb**\n\nProperties and parameters for the workflow are stored in a unique file to update in order to change parameters such as compound, dose, time, etc:\n* **props.properties**\n\nThe package source code is contained in the mana folder and can be installed as a python module.\n## Installation:\n### Requirements:\n\n* Python3.9X\n* Java 11\n* Met4j 1.2.2 jar (stored in this repository)\n* CPLEX 12.10 or newer (not required for the test case)\n\n### Installing the package\n\nIf needed, install poetry (package and dependances management):\n\n<code>pip install poetry</code>\n\nThen, from the root directory of the MANA repository, enter the following command:\n\n<code>pip install . -e</code>\n\n### Launching the main jupyter notebook (test case)\n\nFrom the root directory of the MANA repository, enter the following command:\n\n<code>python3 -m jupyterlab master_notebook.ipynb</code>\n\nOnce JupyterLab opened in your navigator, you can click on "Run", then click on "Run All Cells" as illustrated below.\n\n![Alt text](readme_figures/jupyterlab_interface_example.png)\n\nIt will perform the complete workflow on the test case (PHH exposed to amiodarone during 24h and associated controls).\nThe notebook will pause near the end of the workflow waiting for you to provide the desired number of clusters during the hierarchical clustering step.\n\n## Localisation of the main results files:\n\n[Annotated cluster 1](tests/analysis/clusters_annotation_tables/amiodarone_24_hr_extracellexclude_cluster1_table.xlsx)\n\n[Annotated cluster 2](tests/analysis/clusters_annotation_tables/amiodarone_24_hr_extracellexclude_cluster2_table.xlsx)\n\n[Subnetwork 1 reactions list](tests/analysis/subnetwork_reactions/amiodarone_24_hr_extracellexclude_cluster1_undirected_r2_noisecond_extracell.txt)\n\n[Subnetwork 2 reactions list](tests/analysis/subnetwork_reactions/amiodarone_24_hr_extracellexclude_cluster2_undirected_r2_noisecond_extracell.txt)\n\n## Visualisation with MetExploreViz:\n\nTo visualise cluster\'s subnetworks in MetExploreViz, follow these steps:\n* go to https://metexplore.toulouse.inrae.fr/metexplore2/, then click on "Start MetExplore"\n* In the BioSources tab, find and left click on "Homo Sapiens", then double click on "Swainston2016 - Reconstruction of human metabolic network (Recon 2.2)"\n* Once loading is finished, left click on "OMICS", then on "Mapping -> From omics", load the desired subnetwork reactions .txt file\n* Change Object from "Metabolites" to "Reaction" and left click on "Map"\n* Once the mapping is finished, click on the "Network Data" tab then on the "Reactions" tab.\n* Filter reactions to keep only mapped reactions:\n    ![Alt text](readme_figures/filter_reactions.png)\n* Right click and left click on "Copy all to cart"\n* Create the network from the cart as shown below:\n    ![Alt text](readme_figures/graph_from_cart.png)\n\nNext, you will be able to remove side compounds, move nodes and map new information on the visualisation.\nMore information available in MetExplore documentation (https://metexplore.toulouse.inrae.fr/metexplore-doc/index.php) and MetExploreViz documentation (https://metexplore.toulouse.inrae.fr/metexploreViz/doc/index.php)\n\n\n## Contact:\nLouison Fresnais: fresnaislouison@gmail.com\n\nMetExplore/MetExploreViz team: contact-metexplore@inra.fr\n',
    'author': 'Louison Fresnais',
    'author_email': 'fresnaislouison@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
