# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beeflow',
 'beeflow.client',
 'beeflow.common',
 'beeflow.common.build',
 'beeflow.common.cloud',
 'beeflow.common.crt',
 'beeflow.common.db',
 'beeflow.common.gdb',
 'beeflow.common.integration',
 'beeflow.common.parser',
 'beeflow.common.worker',
 'beeflow.data.cwl.bee_workflows.pennant-build',
 'beeflow.data.cwl.cwl_validation.ml-workflow.example-1',
 'beeflow.data.cwl.cwl_validation.ml-workflow.machine_learning',
 'beeflow.data.dockerfiles.pennant-graph',
 'beeflow.scheduler',
 'beeflow.task_manager',
 'beeflow.tests',
 'beeflow.wf_manager',
 'beeflow.wf_manager.common',
 'beeflow.wf_manager.resources']

package_data = \
{'': ['*'],
 'beeflow': ['data/cloud_templates/*',
             'data/cwl/*',
             'data/cwl/bee_workflows/*',
             'data/cwl/bee_workflows/blast/*',
             'data/cwl/bee_workflows/blast/input/*',
             'data/cwl/bee_workflows/cat-grep-fail/*',
             'data/cwl/bee_workflows/clamr-ci/*',
             'data/cwl/bee_workflows/clamr-ffmpeg-build_script/*',
             'data/cwl/bee_workflows/clamr-wf-chicoma/*',
             'data/cwl/bee_workflows/clamr-wf-noyaml/*',
             'data/cwl/bee_workflows/clamr-wf-noyaml/lsf-charliecloud/*',
             'data/cwl/bee_workflows/clamr-wf-noyaml/slurm-charliecloud/*',
             'data/cwl/bee_workflows/clamr-wf-noyaml/slurm-singularity/*',
             'data/cwl/bee_workflows/clamr-wf-singularity/*',
             'data/cwl/bee_workflows/clamr-wf-summit/*',
             'data/cwl/bee_workflows/clamr-wf-use-container/*',
             'data/cwl/bee_workflows/clamr-wf/*',
             'data/cwl/bee_workflows/comd-mpi/*',
             'data/cwl/bee_workflows/lulesh-mpi-multi-file/*',
             'data/cwl/bee_workflows/lulesh-mpi/*',
             'data/cwl/bee_workflows/nwchem-mpi/*',
             'data/cwl/bee_workflows/pennant/*',
             'data/cwl/bee_workflows/simple-workflows/*',
             'data/cwl/bee_workflows/simple-workflows/grep-wordcount/*',
             'data/cwl/cwl_validation/*',
             'data/cwl/cwl_validation/builder/*',
             'data/cwl/cwl_validation/grep-wordcount/*',
             'data/dockerfiles/*',
             'data/dockerfiles/comd-pmix-support/*',
             'enhanced_client/*',
             'enhanced_client/data/*',
             'enhanced_client/renderer/*',
             'enhanced_client/renderer/img/*',
             'enhanced_client/renderer/styles/*'],
 'beeflow.tests': ['clamr-wf/*']}

install_requires = \
['APScheduler>=3.6.3,<4.0.0',
 'Flask>=2.0,<3.0',
 'PyYAML>=6.0.1,<7.0.0',
 'celery[redis,sqlalchemy]>=5.3.4,<6.0.0',
 'cffi>=1.15.1,<2.0.0',
 'cwl-utils>=0.16,<0.17',
 'flask_restful==0.3.9',
 'gunicorn>=20.1.0,<21.0.0',
 'jsonpickle>=2.2.0,<3.0.0',
 'neo4j>=1.7.4,<2.0.0',
 'python-daemon>=2.3.1,<3.0.0',
 'requests-unixsocket>=0.3.0,<0.4.0',
 'requests<2.29.0',
 'typer>=0.5.0,<0.6.0']

extras_require = \
{'cloud_extras': ['google-api-python-client>=2.66.0,<3.0.0',
                  'python-openstackclient>=6.0.0,<7.0.0',
                  'python-heatclient>=3.1.0,<4.0.0']}

entry_points = \
{'console_scripts': ['beecloud = beeflow.cloud_launcher:main',
                     'beeflow = beeflow.client.bee_client:main']}

setup_kwargs = {
    'name': 'hpc-beeflow',
    'version': '0.1.7',
    'description': 'A software package for containerizing HPC applications and managing job workflows',
    'long_description': 'BEE: Build and Execution Environment\n************************************\n\nBEE is a workflow orchestration system designed to build containerized HPC applications and orchestrate workflows across HPC and cloud systems. BEE has adopted the Common Workflow Language (`CWL <https://www.commonwl.org/>`_) for specifying workflows. Complex scientific workflows specified by CWL are managed and visualized through a graph database, giving the user the ability to monitor the state of each task in the workflow. BEE runs jobs using the workload scheduler (i.e. Slurm or LSF) on the HPC system that tasks are specified to run on.\n\nBEE workflows can be archived for provenance and reproducibility. BEE can orchestrate workflows with containerized applications or those built locally on a system. However, there are advantages to containerizing an application.\n\nA container is a package of code (usually binaries) and all of that code\'s dependencies (libraries, etc.). Once built, this container can be run on many different platforms.\n\nContainers provide many benefits:\n\n* Users can choose their own software stack (libraries, compilers, etc.) and not be bound by the currently installed environment on any one machine.\n\n* Codes can be run portably across numerous platforms--all dependencies will be downloaded and installed at run time.\n\n* Entire **workflow** environments can be built into one or more containers. A user can include visualization and analysis tools along with the application. They will all work together as the application runs.\n\n* Provenance and history can be tracked by storing containers in a historical repository. At any time, an older container can be rerun (all of its dependencies are stored with it). Execution is repeatable and interactions between software components can be tracked.\n\n* Functional testing can be performed on smaller, dissimilar machines--there is no real need to test on the actual HPC platform (performance testing obviously requires target hardware).\n\n\nBEE Sites\n=========\n\n* Documentation: `https://lanl.github.io/BEE/ <https://lanl.github.io/BEE/>`_\n\n* Github: `https://github.com/lanl/BEE <https://github.com/lanl/BEE>`_\n\n\nContact\n=======\n\n\nFor bugs and problems report, suggestions and other general questions regarding the BEE project, email questions to `bee-dev@lanl.gov <bee-dev@lanl.gov>`_.\n\n\nContributors:\n==========================\n\n* Steven Anaya - `Boogie3D <https://github.com/Boogie3D>`_\n* Paul Bryant - `paulbry <https://github.com/paulbry>`_\n* Rusty Davis - `rstyd <https://github.com/rstyd>`_\n* Jieyang Chen - `JieyangChen7 <https://github.com/JieyangChen7>`_\n* Krishna Chilleri - `Krishna Chilleri <https://github.com/kchilleri>`_\n* Patricia Grubel - `pagrubel <https://github.com/pagrubel>`_\n* Qiang Guan - `guanxyz <https://github.com/guanxyz>`_\n* Ragini Gupta - `raginigupta6 <https://github.com/raginigupta6>`_\n* Andres Quan - `aquan9 <https://github.com/aquan9>`_\n* Quincy Wofford - `qwofford <https://github.com/qwofford>`_\n* Tim Randles - `trandles-lanl <https://github.com/trandles-lanl>`_\n* Jacob Tronge - `jtronge <https://github.com/jtronge>`_\n\nConcept and Design Contributors\n\n* James Ahrens\n* Allen McPherson\n* Li-Ta Lo\n* Louis Vernon\n\n\nContributing\n==========================\n\nThe BEE project adheres to style guidelines specified in `setup.cfg <https://github.com/lanl/BEE/blob/master/setup\\.cfg>`_. Before attempting to commit and push changes, please install our pre-commit githooks by running the following command in project root:\n\nIf using `git --version` >= 2.9:\n    git config core.hooksPath .githooks\n\nOtherwise:\n    cp .githooks/* .git/hooks/\n\nUsing these git hooks will ensure your contributions adhere to style guidelines required for contribution. You will need to repeat these steps for every `BEE` repo you clone.\n\n\nRelease\n==========================\n\nThis software has been approved for open source release and has been assigned **BEE C17056**.\n\nCopyright\n==========================\nLicense can be found `here <https://github.com/lanl/BEE/blob/master/LICENSE>`_\n\n\nPublications\n==========================\n\n- An HPC-Container Based Continuous Integration Tool for Detecting Scaling and Performance Issues in HPC Applications, IEEE Transactions on Services Computing, 2024, `DOI: 10.1109/TSC.2023.3337662 <https://doi.ieeecomputersociety.org/10.1109/TSC.2023.3337662>`_\n- BEE Orchestrator: Running Complex Scientific Workflows on Multiple Systems, HiPC, 2021, `DOI: 10.1109/HiPC53243.2021.00052 <https://doi.org/10.1109/HiPC53243.2021.00052>`_\n- "BeeSwarm: Enabling Parallel Scaling Performance Measurement in Continuous Integration for HPC Applications", ASE, 2021, `DOI: 10.1109/ASE51524.2021.9678805 <https://www.computer.org/csdl/proceedings-article/ase/2021/033700b136/1AjTjgnW2pa#:~:text=10.1109/ASE51524.2021.9678805>`_\n- "BeeFlow: A Workflow Management System for In Situ Processing across HPC and Cloud Systems", ICDCS, 2018, `DOI: 10.1109/ICDCS.2018.00103 <https://ieeexplore.ieee.org/abstract/document/8416366>`_\n- "Build and execution environment (BEE): an encapsulated environment enabling HPC applications running everywhere", IEEE BigData, 2018, `DOI: 10.1109/BigData.2018.8622572 <https://ieeexplore.ieee.org/document/8622572>`_\n',
    'author': 'BEE-LANL Dev Team',
    'author_email': 'bee-dev@lanl.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lanl/BEE',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8.3,<=3.12.2',
}


setup(**setup_kwargs)
