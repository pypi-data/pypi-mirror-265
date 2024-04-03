# ---------------------------------------------------------------------
# Copyright (c) 2024 Qualcomm Innovation Center, Inc. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# ---------------------------------------------------------------------
from __future__ import annotations

from typing import Dict, List, Optional

import numpy as np
import torch

from qai_hub_models.evaluators.base_evaluators import BaseEvaluator
from qai_hub_models.evaluators.classification_evaluator import ClassificationEvaluator
from qai_hub_models.utils.base_model import BaseModel
from qai_hub_models.utils.input_spec import InputSpec
from qai_hub_models.utils.quantization import get_image_quantization_samples

MODEL_ASSET_VERSION = 1
MODEL_ID = __name__.split(".")[-2]
IMAGENET_DIM = 224


class ImagenetClassifier(BaseModel):
    """
    Base class for all Imagenet Classifier models within QAI Hub Models.
    """

    def __init__(
        self,
        net: torch.nn.Module,
        transform_input: bool = False,
    ):
        """
        Basic initializer which takes in a pretrained classifier network.
        Subclasses can choose to implement their own __init__ and forward methods.
        """
        super().__init__()
        self.transform_input = transform_input
        self.net = net
        self.eval()

    # Type annotation on image_tensor causes aimet onnx export failure
    def forward(self, image_tensor):
        """
        Predict class probabilities for an input `image`.

        Parameters:
            image: A [1, 3, 224, 224] image.
                   Assumes image has been resized and normalized using the
                   standard preprocessing method for PyTorch Imagenet models.

                   Pixel values pre-processed for encoder consumption.
                   Range: float[0, 1]
                   3-channel Color Space: RGB

        Returns:
            A [1, 1000] where each value is the log-likelihood of
            the image belonging to the corresponding Imagenet class.
        """
        if self.transform_input:
            # This is equivalent but converts better than the built-in.
            # transform_input should be turned off in torchvision model.
            shape = (1, 3, 1, 1)
            scale = torch.tensor([0.229 / 0.5, 0.224 / 0.5, 0.225 / 0.5]).reshape(shape)
            bias = torch.tensor(
                [(0.485 - 0.5) / 0.5, (0.456 - 0.5) / 0.5, (0.406 - 0.5) / 0.5]
            ).reshape(shape)
            image_tensor = image_tensor * scale + bias
        return self.net(image_tensor)

    def get_evaluator(self) -> BaseEvaluator:
        return ClassificationEvaluator()

    @staticmethod
    def get_input_spec() -> InputSpec:
        """
        Returns the input specification (name -> (shape, type). This can be
        used to submit profiling job on Qualcomm® AI Hub.
        """
        return {"image_tensor": ((1, 3, IMAGENET_DIM, IMAGENET_DIM), "float32")}

    @classmethod
    def from_pretrained(
        cls,
        weights: Optional[str] = None,
    ) -> "ImagenetClassifier":
        net = cls.model_builder(weights=weights or cls.DEFAULT_WEIGHTS)
        return cls(net)

    def sample_inputs(
        self, input_spec: InputSpec | None = None
    ) -> Dict[str, List[np.ndarray]]:
        samples = get_image_quantization_samples()
        return dict(image_tensor=[samples[:1].numpy()])
