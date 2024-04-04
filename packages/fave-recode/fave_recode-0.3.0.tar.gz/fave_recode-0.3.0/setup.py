# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fave_recode']

package_data = \
{'': ['*'], 'fave_recode': ['resources/*']}

install_requires = \
['aligned-textgrid>=0.6.4,<0.7.0',
 'cerberus>=1.3.5,<2.0.0',
 'click>=8.1.7,<9.0.0',
 'cloup>=3.0.2,<4.0.0',
 'pyyaml>=6.0,<7.0']

entry_points = \
{'console_scripts': ['fave_recode = fave_recode.fave_recode:fave_recode']}

setup_kwargs = {
    'name': 'fave-recode',
    'version': '0.3.0',
    'description': 'A package for recoding Praat TextGrids',
    'long_description': '# Getting started with `fave-recode`\n\n\n![PyPI](https://img.shields.io/pypi/v/fave-recode.png)\n[![codecov](https://codecov.io/gh/Forced-Alignment-and-Vowel-Extraction/fave-recode/graph/badge.svg?token=C23B1H3DAX)](https://codecov.io/gh/Forced-Alignment-and-Vowel-Extraction/fave-recode)\n[![Maintainability](https://api.codeclimate.com/v1/badges/2375ddfef5d77ba1681d/maintainability.png)](https://codeclimate.com/github/Forced-Alignment-and-Vowel-Extraction/fave-recode/maintainability)\n[![FAVE Python\nCI](https://github.com/Forced-Alignment-and-Vowel-Extraction/fave-recode/actions/workflows/test-and-run.yml/badge.svg?branch=dev)](https://github.com/Forced-Alignment-and-Vowel-Extraction/fave-recode/actions/workflows/test-and-run.yml)\n[![Build\nDocs](https://github.com/Forced-Alignment-and-Vowel-Extraction/fave-recode/actions/workflows/build-docs.yml/badge.svg)](https://forced-alignment-and-vowel-extraction.github.io/fave-recode/)\n[![DOI](https://zenodo.org/badge/605740158.svg)](https://zenodo.org/badge/latestdoi/605740158)\n\nThe idea behind `fave-recode` is that no matter how much you may adjust\nthe dictionary of a forced-aligner, you may still want to make\nprogrammatic changes to the output.\n\n## Installation\n\nYou can install `fave-recode` at your system’s command line with `pip`.\n\n``` bash\npip install fave-recode\n```\n\n## Basic usage\n\nInstallation of the `fave-recode` python package makes the `fave_recode`\nexecutable, which can also be run at the command line. You can get help\nwith `--help`\n\n``` bash\nfave_recode --help\n```\n\n    Usage: fave_recode [OPTIONS]\n\n    Inputs: [at least 1 required]\n      File inputs. Either a single file with -i or a path with -p. Not both.\n      -i, --input_file FILENAME  single input file\n      -p, --input_path PATH      Path to a set of files\n\n    Outputs:\n      -o, --output_file TEXT     An output file name\n      -d, --output_dest PATH     An output directory\n\n    Other options:\n      -a, --parser TEXT          Label set parser. Built in options are cmu_parser\n      -s, --scheme TEXT          Recoding scheme. Built in options are cmu2labov\n                                 and cmu2phila  [required]\n      -r, --recode_stem TEXT     Stem to append to recoded TextGrid file names\n      -t, --target_tier TEXT     Target tier to recode\n      --help                     Show this message and exit.\n\nTo recode a single file, you need to provide `fave_recode` with,\nminimally, the input file (the `-i` flag), and the recoding scheme (with\nthe `-s` flag). There are a few default recoding schemes that come with\n`fave_recode`.\n\n``` bash\nls data\n```\n\n    KY25A_1.TextGrid                 josef-fruehwald_speaker.TextGrid\n\n``` bash\nfave_recode -i data/josef-fruehwald_speaker.TextGrid -s cmu2phila -a cmu_parser\n\nls data\n```\n\n    KY25A_1.TextGrid\n    josef-fruehwald_speaker.TextGrid\n    josef-fruehwald_speaker_recoded.TextGrid\n',
    'author': 'JoFrhwld',
    'author_email': 'JoFrhwld@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://forced-alignment-and-vowel-extraction.github.io/fave-recode',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
