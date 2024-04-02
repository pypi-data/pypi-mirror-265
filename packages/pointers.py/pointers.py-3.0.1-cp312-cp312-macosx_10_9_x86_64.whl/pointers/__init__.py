if __import__("sys").implementation.name != "cpython":
    # using __import__ to make sure sys isnt exported
    raise Exception(
        "pointers.py is only supported on cpython",
    )

from ._utils import force_set_attr
from .api_bindings import *
from .base_pointers import (
    BaseAllocatedPointer, BaseCPointer, BaseObjectPointer, BasePointer,
    BasicPointer, Dereferencable, IterDereferencable, Sized
)
from .bindings import *
from .c_pointer import (
    TypedCPointer, VoidPointer, array, cast, to_c_ptr, to_func_ptr,
    to_struct_ptr, to_voidp
)
from .calloc import AllocatedArrayPointer, calloc
from .custom_binding import binding, binds
from .decay import decay, decay_annotated, decay_wrapped
from .exceptions import (
    AllocationError, DereferenceError, FreedMemoryError,
    InvalidBindingParameter, InvalidSizeError, NullPointerError,
    SegmentViolation, VariableLifetimeError
)
from .magic import _
from .malloc import AllocatedPointer, free, malloc, realloc
from .object_pointer import Pointer, to_ptr
from .stack_pointer import (
    StackAllocatedPointer, acquire_stack_alloc, stack_alloc
)
from .std_structs import DivT, Lconv, LDivT, Tm
from .structure import Struct, StructPointer
from .util import NULL, Nullable, handle, raw_type, struct_cast, stop_handler
from .var_pointer import VarPointer, to_var_ptr

__version__ = "3.0.0"
__license__ = "MIT"
