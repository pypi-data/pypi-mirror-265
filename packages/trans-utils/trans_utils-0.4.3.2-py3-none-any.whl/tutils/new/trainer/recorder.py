"""
This is a template for Tester
"""

import torch
import numpy as np
from tutils import tfunctime
from typing import Dict, List, Tuple


class Recorder(object):
    def __init__(self, logger=None, config=None, reduction="mean", inclusion=None):
        super(Recorder, self).__init__()
        self.logger = logger
        self.config = config
        self.loss_list = []
        self.loss_keys = None
        self.reduction = reduction
        self.inclusion = inclusion

    def clear(self):
        self.loss_list.clear()
        self.loss_keys = None

    def record(self, loss:dict) -> None:
        assert type(loss) == dict, f"Got {loss}"
        # print("debug record", loss)
        if self.loss_keys is None:
            self.loss_list = []
            self.loss_keys = loss.keys()
        l_list = []
        for key, value in loss.items():
            if isinstance(value, torch.Tensor):
                l_list.append(value.detach().cpu().item())
            elif isinstance(value, (str, bool, list, dict)):
                # print()
                pass
            elif isinstance(value, (np.ndarray, np.float64, np.float32, int, float)):
                l_list.append(float(value))
            else:
                print("debug??? type Error? , got ", type(value))
                print("debug??? ", key, value)
                raise ValueError
                l_list.append(float(value))
        self.loss_list.append(l_list)

    def _record(self, loss):
        if isinstance(loss, torch.Tensor):
            loss = loss.detach().cpu().item()
            if self.loss_list is None:
                self.loss_list = []
            self.loss_list.append(loss)
        elif isinstance(loss, list):
            for i, lossi in enumerate(loss):
                if type(lossi) == torch.Tensor:
                    loss[i] = lossi.detach().cpu().item()
            if self.loss_list is None:
                self.loss_list = []
            self.loss_list.append(loss)
        elif isinstance(loss, dict):
            if self.loss_list is None:
                self.loss_list = []
                self.loss_keys = loss.keys
            l_list = []
            for lossi, value in loss.items():
                if type(lossi) == torch.Tensor:
                    l_list.append(lossi.detach().cpu().item())
            self.loss_list.append(l_list)

    def cal_metrics(self):
        temp = np.array(self.loss_list)
        if self.reduction == "mean":
            res = temp.mean(axis=0)
        elif self.reduction == "sum":
            res = temp.sum(axis=0)
        else:
            raise ValueError
        # print("debug mean", mean, temp, self.loss_keys)
        
        _dict = {k: res[i] for i, k in enumerate(self.loss_keys)}
        return _dict


class DistRecorder(Recorder):
    def __init__(self, is_master, logger=None, config=None, reduction="mean", inclusion=None):
        super().__init__(logger, config, reduction, inclusion)
        self.is_master = is_master
    
    def clear(self):
        if not self.is_master: return 
        return super().clear()

    def record(self, loss:dict) -> None:
        if not self.is_master: return         
        return super().record(loss)
    
    def _record(self, loss):
        if not self.is_master: return         
        return super()._record(loss)

    def cal_metrics(self):
        if not self.is_master: return   
        return super().cal_metrics()


class EpochRecorder(object):
    def __init__(self, logger, config, mode="dec"):
        # mode in ["dec", "inc"]
        self.logger = logger
        self.config = config
        self.best_epoch = None
        self.best_value = None
        self.epoch_list = []
        self.value_list = []
        self.mode = mode
        if mode == "dec":
            self.comp = self._less
        else:
            self.comp = self._greater

    def _less(self, a, b):
        if a < b: return True
        else: return False

    def _greater(self, a, b):
        if a > b: return True
        else: return False

    def record_and_return(self, epoch, value):
        if self.best_epoch is None:
            self.best_epoch = epoch
            self.best_value = value
        # self.best_epoch.append(epoch)
        # self.best_value.append(value)
        if self.comp(value, self.best_epoch):
            self.best_epoch = epoch
            self.best_value = value
            return True
        else:
            return False


class Tester(object):
    def __init__(self, args, config, logger):
        self.args = args
        self.config = config
        self.logger = logger
        self.evaluater = Recorder(logger, config)
        self.model = None

    def test(self, net=None, epoch=None, train="", dump_label=False):
        self.evaluater.reset()
        self.model = net
        """
        ...
        """
        mre = self.evaluater.cal_metrics()
        return mre


