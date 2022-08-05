# YAWNING TITAN

## About The Project
YAWNING TITAN is an abstract, graph based cyber-security simulation environment that supports the training of
intelligent agents for autonomous cyber operations. YAWNING TITAN currently only supports defensive autonomous agents
who face off against probabilistic red agents.

YAWNING TITAN has been designed with the following things in mind:
- Simplicity over complexity
- Minimal Hardware Requirements
- Support for a wide range of algorithms
- Enhanced agent/policy evaluation support
- Flexible environment and game rule setup
- Generation of evaluation episode visualisations (gifs)

YAWNING TITAN was publicly released on 20th July 2022 under MIT licence. It will continue to be developed through the Autonomous Resilient Cyber Defence (ARCD) project, overseen by Dstl.

Feedback on its operation, and suggestions for enhancements, is gratefully received via the Issues tab.

As the YAWNING TITAN project progresses, updates will be posted on this site.

## What's YAWNING TITAN built with

- [OpenAI's Gym](https://gym.openai.com/)
- [Networkx](https://github.com/networkx/networkx)
- [Stable Baselines 3](https://github.com/DLR-RM/stable-baselines3)
- [Rllib (part of Ray)](https://github.com/ray-project/ray)

## Getting Started with YAWNING TITAN

### Pre-Requisites

In order to get YAWNING TITAN installed, you will need to have the following installed:
- `python3.7+`
- `python3-pip`
- `virtualenv`

### Installation
1. Navigate to the YAWNING TITAN folder and create a new python virtual environment
```bash
python3 -m venv <name_of_venv>
```
2. Activate virtual environment
```bash
source <name_of_venv>/bin/activate
```
3. Install `yawning-titan` into the environment along with all of it's dependencies
```bash
python3 -m pip install -e .
```
This will install all of the dependencies including algorithm libraries. These libraries
all use `torch`. If you'd like to install `tensorflow` for use with Rllib, you can do this manually
or install `tensorflow` as an optional dependency by executing the following command `python3 -m pip install -e .[tensorflow]`.

### Documentation

YAWNING TITAN comes with a full set of documentation created using the Sphinx documentation library and these can be built by using the following commands:
> This will require the development dependencies to be installed - You can install these by executing  ``python3 -m pip install -e .[dev]``
```
cd docs
make html
```
This will build the documentation as a collection of HTML files which uses the Read The Docs sphinx theme. Other build options are available but may require additional dependencies such as LaTeX and PDF.
Please refer to the Sphinx documentation for your specific output requirements.

### Example Notebooks

A collection of example notebooks have been provided in `/notebooks` and are the best place to start if you want to get a feel for YAWNING TITAN before builidng the docs and exploring
further.

# License

YAWNING TITAN is released under MIT license. Please see [LICENSE](LICENSE) for details.
