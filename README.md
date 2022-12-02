![Python](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10-blue)
![GitHub](https://img.shields.io/github/license/dstl/YAWNING-TITAN)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/dstl/YAWNING-TITAN/Python%20package)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/dstl/YAWNING-TITAN/build-sphinx-to-github-pages?label=docs)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/dstl/YAWNING-TITAN)
![GitHub commits since latest release (by SemVer)](https://img.shields.io/github/commits-since/dstl/YAWNING-TITAN/latest)
![GitHub issue custom search](https://img.shields.io/github/issues-search?label=active%20bug%20issues&query=repo%3Adstl%2FYAWNING-TITAN%20is%3Aopen%20label%3Abug)
![GitHub issue custom search](https://img.shields.io/github/issues-search?label=active%20feature%20requests&query=repo%3Adstl%2FYAWNING-TITAN%20is%3Aopen%20label%3Afeature_request)
![GitHub Discussions](https://img.shields.io/github/discussions/dstl/YAWNING-TITAN)

# YAWNING-TITAN

## About The Project
YAWNING-TITAN (**YT**) is an abstract, graph based cyber-security simulation environment that supports the training of
intelligent agents for autonomous cyber operations. YAWNING-TITAN currently only supports defensive autonomous agents
who face off against probabilistic red agents.

**YT** has been designed with the following things in mind:
- Simplicity over complexity
- Minimal Hardware Requirements
- Operating System agnostic
- Support for a wide range of algorithms
- Enhanced agent/policy evaluation support
- Flexible environment and game rule configuration
- Generation of evaluation episode visualisations (gifs)

**YT** was publicly released on 20th July 2022 under MIT licence. It will continue to be developed through the Autonomous
Resilient Cyber Defence (ARCD) project, overseen by Dstl.

## Contributing to YAWNING-TITAN
Found a bug, have an idea/feature you'd like to suggest, or just want to get involved with the YT community, please read
our [How to contribute to YAWNING-TITAN?](CONTRIBUTING.md) guidelines.


## What's YAWNING-TITAN built with

- [OpenAI's Gym](https://gym.openai.com/)
- [Networkx](https://github.com/networkx/networkx)
- [Stable Baselines 3](https://github.com/DLR-RM/stable-baselines3)
- [Rllib (part of Ray)](https://github.com/ray-project/ray)


## Getting Started with YAWNING-TITAN

### Pre-Requisites

In order to get **YT** installed, you will need to have the following installed:

- `python3.8+`
- `python3-pip`
- `virtualenv`

**YT** is designed to be OS-agnostic, and thus should work on most variations/distros of Linux, Windows, and MacOS.

### Installation from source
#### 1. Navigate to the YAWNING-TITAN folder and create a new python virtual environment (venv)

```unix
python3 -m venv <name_of_venv>
```

#### 2. Activate the venv

##### Unix
```bash
source <name_of_venv>/bin/activate
```

##### Windows
```powershell
.\<name_of_venv>\Scripts\activate
```

#### 3. Install `yawning-titan` into the venv along with all of it's dependencies

```bash
python3 -m pip install -e .
```


This will install all the dependencies including algorithm libraries. These libraries
all use `torch`. If you'd like to install `tensorflow` for use with Rllib, you can do this manually
or install `tensorflow` as an optional dependency by postfixing the command in step 3 above with the `[tensorflow]` extra. Example:

```bash
python3 -m pip install -e .[tensorflow]
```

### Development Installation
To install the development dependencies, postfix the command in step 3 above with the `[dev]` extra. Example:

```bash
python3 -m pip install -e .[dev]
```

## Application Directories

Upon install, **YT** creates a set of application directories, both hidden for **YT** use, and visible for user use. The
created directory trees for Linux, Windows, and MacOS operating systems are detailed below:

##### Linux
```
~/
├─ .cache/
│  ├─ yawning_titan/
│  │  ├─ log/
├─ .config/
│  ├─ yawning_titan/
├─ .local/
│  ├─ share/
│  │  ├─ yawning_titan/
│  │  │  ├─ app_images/
│  │  │  ├─ db/
│  │  │  ├─ docs/
├─ yawning_titan/
│  ├─ agents/
│  ├─ game_modes/
│  ├─ images/
│  ├─ notebooks/
```

##### Windows

```
~/
├─ AppData/
│  ├─ yawning_titan/
│  │  ├─ app_images/
│  │  ├─ config/
│  │  ├─ db/
│  │  ├─ docs/
│  │  ├─ logs/
├─ yawning_titan/
│  ├─ agents/
│  ├─ game_modes/
│  ├─ images/
│  ├─ notebooks/
```

##### MacOS
```
~/
├─ Library/
│  ├─ Application Support/
│  │  ├─ Logs/
│  │  │  ├─ yawning_titan/
│  │  │  │  ├─ log/
│  │  ├─ Preferences/
│  │  │  ├─ yawning_titan/
│  │  ├─ yawning_titan/
│  │  │  ├─ app_images/
│  │  │  ├─ db/
│  │  │  ├─ docs/
├─ yawning_titan/
│  ├─ agents/
│  ├─ game_modes/
│  ├─ images/
│  ├─ notebooks/
```

## Documentation

**YT** comes with a full set of documentation created using the Sphinx documentation library and are hosted on GitHub
pages at [https://dstl.github.io/YAWNING-TITAN](https://dstl.github.io/YAWNING-TITAN/index.html).

These docs can also be built manually from the cloned repo by using the following commands:
> This will require the development dependencies to be installed, see [Development Installation](#development-installation)

##### Unix
```bash
cd docs
make html
```

##### Windows
```powershell
cd docs
.\make.bat html
```


This will build the documentation as a collection of HTML files which uses the Read The Docs sphinx theme. Other build
options are available but may require additional dependencies such as LaTeX and PDF. Please refer to the Sphinx documentation
for your specific output requirements.

## Example Notebooks

A collection of example notebooks have been provided. The original versions of these notebooks stored in
[`yawning_titan/notebooks/_package_data`](yawning_titan/notebooks/_package_data) and are copied over to the newly created
users notebooks application directory (`~/yawning_titan/notebooks`) at install. These are the best place to start if you
want to get a feel for **YT** before builidng the docs and exploring further. If the notebooks become corrupted in the
users notebooks application directory, they can be reset running the following commands from an interactive Python
session on your venv:

```python
from yawning_titan.notebooks.jupyter import reset_default_jupyter_notebooks
reset_default_jupyter_notebooks(overwrite_existing=True)
```

## Cite This Work

If you would like to include a citation for **YT** in your work, please cite the paper published at the ICML 2022 ML4Cyber Workshop.
```bibtex
@inproceedings{inproceedings,
 author = {Andrew, Alex and Spillard, Sam and Collyer, Joshua and Dhir, Neil},
 year = {2022},
 month = {07},
 title = {Developing Optimal Causal Cyber-Defence Agents via Cyber Security Simulation},
 maintitle = {International Confernece on Machine Learning (ICML)},
 booktitle = {Workshop on Machine Learning for Cybersecurity (ML4Cyber)}
}
```

# License

YAWNING-TITAN is released under MIT license. Please see [LICENSE](LICENSE) for details.
