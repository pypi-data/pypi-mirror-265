# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved

from typing import Dict
from tritonclient.grpc import model_config_pb2
from google.protobuf import text_format, json_format


class ModelConfig:
    """
    ModelConfig For Triton Model
    """

    def __init__(self, model_config):
        self._model_config = model_config

    def is_ensemble(self) -> bool:
        """
        return if model is ensemble
        Returns:
            bool: _description_
        """
        return getattr(self._model_config, "platform") == "ensemble"

    def as_dict(self) -> Dict:
        """
        return model config as dict
        Returns:
            Dict: _description_
        """
        return json_format.MessageToDict(self._model_config)

    def get_ensemble_steps(self):
        """
        get ensemble steps
        """
        if not self.is_ensemble():
            raise ValueError("Model config is not an ensemble")

        model_config_dict = self.as_dict()
        if (
            "ensembleScheduling" not in model_config_dict
            or "step" not in model_config_dict["ensembleScheduling"]
            or len(model_config_dict["ensembleScheduling"]["step"]) < 1
        ):
            raise ValueError("Model ensembleScheduling is not valid")

        scheduling_step = {}
        try:
            for step in model_config_dict["ensembleScheduling"]["step"]:
                scheduling_step[step["modelName"]] = step["modelVersion"]
        except Exception:
            raise ValueError("Model ensembleScheduling is not valid")

        return scheduling_step

    def set_scheduling_model_version(self, model_name, model_version):
        """
        set scheduling model version
        """
        if not self.is_ensemble():
            raise ValueError("Model config is not an ensemble")

        model_config_dict = self.as_dict()
        try:
            for step in model_config_dict["ensembleScheduling"]["step"]:
                if step["modelName"] == model_name:
                    step["modelVersion"] = model_version
        except Exception as e:
            raise ValueError("Set model version failed {}".format(e))

        self._model_config = ModelConfig.create_from_dict(
            model_config_dict
        )._model_config

    def set_model_input_field(
        self, model_input_field_name, model_input_field_key, model_input_field_value
    ):
        """
        set model input field
        :param model_input_field_name: filed name eg.image,x
        :param model_input_field_key: filed key eg.dims,data_type
        :param model_input_field_value: filed value eg.[1,3,512,512],TYPE_FP32
        """
        try:
            model_config_dict = self.as_dict()
            for input_field in model_config_dict["input"]:
                if input_field["name"] == model_input_field_name:
                    input_field[model_input_field_key] = model_input_field_value
        except Exception as e:
            raise ValueError("Set model input field failed {}".format(e))

        self._model_config = ModelConfig.create_from_dict(
            model_config_dict
        )._model_config

    def set_model_output_field(
        self, model_output_field_name, model_output_field_key, model_output_field_value
    ):
        """
        set model output field
        :param model_output_field_name: filed name eg.image,x
        :param model_output_field_key: filed key eg.dims,data_type
        :param model_output_field_value: filed value eg.[1,3,512,512],TYPE_FP32
        """
        try:
            model_config_dict = self.as_dict()
            for output_field in model_config_dict["output"]:
                if output_field["name"] == model_output_field_name:
                    output_field[model_output_field_key] = model_output_field_value
        except Exception as e:
            raise ValueError("Set model output field failed {}".format(e))

        self._model_config = ModelConfig.create_from_dict(
            model_config_dict
        )._model_config

    def write_to_file(self, model_config_path, bs):
        """
        write model config to file
        """
        try:
            model_config_bytes = text_format.MessageToBytes(
                self._model_config, as_utf8=True
            )
            bs.write_file(model_config_path, model_config_bytes)
        except Exception as e:
            raise ValueError("Model config write to file error:{}".format(e))

    @staticmethod
    def create_from_dict(model_config_dict):
        """
        create model config from dict
        """
        return ModelConfig(
            json_format.ParseDict(model_config_dict, model_config_pb2.ModelConfig())
        )

    @staticmethod
    def create_from_text(model_config_text):
        """
        create model config from text
        """
        return ModelConfig(
            text_format.Parse(model_config_text, model_config_pb2.ModelConfig())
        )

    @staticmethod
    def create_from_file(model_config_path, bs):
        """
        create model config from file
        """
        if not bs.exist(model_config_path):
            raise FileNotFoundError(
                "Model config path: {} not found".format(model_config_path)
            )
        raw_str = bs.read_file(model_config_path)
        return ModelConfig.create_from_text(raw_str)
