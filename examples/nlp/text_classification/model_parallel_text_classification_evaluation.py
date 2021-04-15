# Copyright (c) 2020, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This script runs model parallel text classification evaluation.
"""
from nemo.collections.nlp.models.nlp_model import NLPDDPPlugin
import pytorch_lightning as pl
from omegaconf import DictConfig

from nemo.collections.nlp.models.text_classification import TextClassificationModel
from nemo.core.config import hydra_runner
from nemo.utils import logging
from nemo.utils.exp_manager import exp_manager


@hydra_runner(config_path="conf", config_name="text_classification_config")
def main(cfg: DictConfig) -> None:
    logging.info(f'\nConfig Params:\n{cfg.pretty()}')
    trainer = pl.Trainer(plugins=[NLPDDPPlugin()], **cfg.trainer)
    exp_manager(trainer, cfg.get("exp_manager", None))

    model = TextClassificationModel.restore_from(cfg.model.nemo_path, trainer=trainer)
    # model.setup_training_data(train_data_config=cfg.model.train_ds)
    # model.setup_validation_data(val_data_config=cfg.model.validation_ds)
    model.setup_test_data(test_data_config=cfg.model.test_ds)
    # model.setup_optimization(cfg.model.optim)

    trainer.test(model=model, ckpt_path=None)


if __name__ == '__main__':
    main()
