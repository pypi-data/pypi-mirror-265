# KTbench

KTbench is a Python library for benchmarking Knowledge Tracing (KT) models. It provides a framework for evaluating the performance of various KT models.

## Installation
Inside the project folder, run

```console
pip install -e .
```

## Usage

```console 
python ./baseleine/run.py
```

By default a ".ktbench" folder is created containing the experiment logs.

```
.ktbench
└── dataset_name
    └── model_name
        └── training_time_stamp
            ├── test.yaml          # Contains results on the test set.
            └── valid_fold_k.yaml  # Contains validation results on the kth fold during training.
```
