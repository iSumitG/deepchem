"""
Script that trains multitask models on Tox21 dataset.
"""
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

import os
import shutil
import numpy as np
import deepchem as dc
from tox21_datasets import load_tox21

# Only for debug!
np.random.seed(123)

# Load Tox21 dataset
n_features = 1024
tox21_tasks, tox21_datasets, transformers = load_tox21()
train_dataset, valid_dataset, test_dataset = tox21_datasets

# Fit models
metric = dc.metrics.Metric(dc.metrics.roc_auc_score, np.mean,
                           mode="classification")

robust_classifier_model = dc.models.RobustMultitaskClassifier(
    len(tox21_tasks), n_features, bypass_layer_sizes=[30],
    bypass_weight_init_stddevs=[.02],
    bypass_bias_init_consts=[1.],
    bypass_dropouts=[.5],
    dropouts=[.4],
    learning_rate=0.002, weight_init_stddevs=[1.],
    batch_size=50, verbosity="high")
model = dc.models.TensorflowModel(robust_classifier_model)

# Fit trained model
model.fit(train_dataset)
model.save()

print("Evaluating model")
train_scores = model.evaluate(train_dataset, [metric], transformers)
valid_scores = model.evaluate(valid_dataset, [metric], transformers)

print("Train scores")
print(train_scores)

print("Validation scores")
print(valid_scores)
