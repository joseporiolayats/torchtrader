# TorchTrader
![Tests](https://github.com/joseporiolayats/torchtrader/actions/workflows/tests.yml/badge.svg)
![Docs](https://github.com/joseporiolayats/torchtrader/actions/workflows/mkdocs.yml/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/joseporiolayats/torchtrader/badge.svg?branch=master)](https://coveralls.io/github/joseporiolayats/torchtrader?branch=master)

# UNDER HEAVY DEVELOPMENT.
# REFERENCE PURPOSES ONLY.


**TorchTrader** is an automated framework for trading assets using bots which take decisions based on deep learning algorithms.

Currently using Pytorch 2 as the deep-learning backend.

## What's the aim?
TorchTrader is a trading framework which includes actual machine-learning algorithms for automated decision making with scripted strategies and runnable bots for each one

## Development
At the first stage, some strategies will have the hyperparameters tuned automagically by AI. This training phase takes time and compute power, so be aware to use GPU or host it in a cloud GPU service.

## Work-modes
TorchTrader can operate in many ways, separate or simultaneous.
- Watcher: Watch and plot many technical analysis indicators.
- Quant: Discover strategies and tune them into profitable actions.
- High Frequency Trading (HFT): Operate in all the markets desired with the selected strategies.

The strategies

### Computation
It will be focused on using CUDA as strongly as possible, but there will be support also for CPU training and inference of new models

### Environment
I'll be using Poetry for package management and woking with a venv without conda.

### Deployment
It is intended to be Docker ready for fast deployment with optimized docker-compose and docker image.

### Documentation
Full project documentation is here https://joseporiolayats.github.io/torchtrader


### Testing Tools used with pre-commit and GitHub Actions
- pytest
- pytest-cov
- tox
- flake8
- mypy
- nbqa

### Directory structure (cookiecutter data-science)

```
├── LICENSE
├── Makefile           <- Makefile with commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default Sphinx project; see sphinx-doc.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.py           <- Make this project pip installable with `pip install -e`
├── src                <- Source code for use in this project.
│   ├── __init__.py    <- Makes src a Python module
│   │
│   ├── data           <- Scripts to download or generate data
│   │   └── make_dataset.py
│   │
│   ├── features       <- Scripts to turn raw data into features for modeling
│   │   └── build_features.py
│   │
│   ├── models         <- Scripts to train models and then use trained models to make
│   │   │                 predictions
│   │   ├── predict_model.py
│   │   └── train_model.py
│   │
│   └── visualization  <- Scripts to create exploratory and results oriented visualizations
│       └── visualize.py
│
└── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io
```

###### This project structure and CI/CD workflow is heavily inspired from a template I adapted from [Johannes Schmidt's](https://github.com/johschmidt42/python-project-johannes/tree/main)
