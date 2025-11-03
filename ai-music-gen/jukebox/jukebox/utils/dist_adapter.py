try:
    import torch.distributed as dist
    TORCH_DIST_AVAILABLE = dist.is_available()
except ImportError:
    TORCH_DIST_AVAILABLE = False
from enum import Enum

class ReduceOp(Enum):
    SUM = 0,
    PRODUCT = 1,
    MIN = 2,
    MAX = 3

    def ToDistOp(self):
        return {
            self.SUM: dist.ReduceOp.SUM,
            self.PRODUCT: dist.ReduceOp.PRODUCT,
            self.MIN: dist.ReduceOp.MIN,
            self.MAX: dist.ReduceOp.MAX
        }[self]

def is_available():
    return False  # Always return False for single-process CPU runs

def get_rank():
    return 0

def get_world_size():
    return 1

def barrier():
    pass

def all_gather(tensor_list, tensor):
    tensor_list[0] = tensor

def all_reduce(tensor, op=ReduceOp.SUM):
    pass

def reduce(tensor, dst, op=ReduceOp.SUM):
    pass

def broadcast(tensor, src):
    pass

def init_process_group(backend, init_method):
    pass

def _get_rank():
    return dist.get_rank()

def _barrier():
    return dist.barrier()

def _get_world_size():
    return dist.get_world_size()

def _all_gather(tensor_list, tensor):
    return dist.all_gather(tensor_list, tensor)

def _all_reduce(tensor, op):
    return dist.all_reduce(tensor, op.ToDistOp())

def _reduce(tensor, dst, op):
    return dist.reduce(tensor, dst, op.ToDistOp())

def _broadcast(tensor, src):
    return dist.broadcast(tensor, src)

def _init_process_group(backend, init_method):
    return dist.init_process_group(backend, init_method)