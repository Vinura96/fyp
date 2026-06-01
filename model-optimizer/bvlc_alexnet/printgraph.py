import time
import onnx, onnx.numpy_helper
from onnx import TensorProto, SparseTensorProto, AttributeProto, ValueInfoProto, TensorShapeProto, \
    NodeProto, ModelProto, GraphProto, OperatorSetIdProto, TypeProto, IR_VERSION
from typing import Text, Sequence, Any, Optional, Dict, Union, TypeVar, Callable, Tuple, List, cast

import numpy as np
model = onnx.load("model.onnx")

def printable_dim(dim):  # type: (TensorShapeProto.Dimension) -> Text
    which = dim.WhichOneof('value')
    assert which is not None
    return str(getattr(dim, which))


def printable_type(t):  # type: (TypeProto) -> Text
    if t.WhichOneof('value') == "tensor_type":
        s = TensorProto.DataType.Name(t.tensor_type.elem_type)
        if t.tensor_type.HasField('shape'):
            if len(t.tensor_type.shape.dim):
                s += str(', ' + 'x'.join(map(printable_dim, t.tensor_type.shape.dim)))
            else:
                s += str(', scalar')
        return s
    if t.WhichOneof('value') is None:
        return ""
    return 'Unknown type {}'.format(t.WhichOneof('value'))


def printable_value_info(v):  # type: (ValueInfoProto) -> Text
    s = '%{}'.format(v.name)
    if v.type:
        s = '{}[{}]'.format(s, printable_type(v.type))
    return s

def printable_node(node, prefix='', subgraphs=False):  # type: (NodeProto, Text, bool) -> Union[Text, Tuple[Text, List[GraphProto]]]
    content = []
    if len(node.output):
        content.append(
            ', '.join(['%{}'.format(name) for name in node.output]))
        content.append('=')
    # To deal with nested graphs
    graphs = []  # type: List[GraphProto]
    printed_attrs = []
    for attr in node.attribute:
        if subgraphs:
            printed_attr, gs = printable_attribute(attr, subgraphs)
            assert isinstance(gs, list)
            graphs.extend(gs)
            printed_attrs.append(printed_attr)
        else:
            printed = printable_attribute(attr)
            assert isinstance(printed, Text)
            printed_attrs.append(printed)
    printed_attributes = ', '.join(sorted(printed_attrs))
    printed_inputs = ', '.join(['%{}'.format(name) for name in node.input])
    if node.attribute:
        content.append("{}[{}]({})".format(node.op_type, printed_attributes, printed_inputs))
    else:
        content.append("{}({})".format(node.op_type, printed_inputs))
    if subgraphs:
        return prefix + ' '.join(content), graphs
    else:
        return prefix + ' '.join(content)

def printable_attribute(attr, subgraphs=False):  # type: (AttributeProto, bool) -> Union[Text, Tuple[Text, List[GraphProto]]]
    content = []
    content.append(attr.name)
    content.append("=")

    def str_float(f):  # type: (float) -> Text
        # NB: Different Python versions print different numbers of trailing
        # decimals, specifying this explicitly keeps it consistent for all
        # versions
        return '{:.15g}'.format(f)

    def str_int(i):  # type: (int) -> Text
        # NB: In Python 2, longs will repr() as '2L', which is ugly and
        # unnecessary.  Explicitly format it to keep it consistent.
        return '{:d}'.format(i)

    def str_str(s):  # type: (Text) -> Text
        return repr(s)

    _T = TypeVar('_T')  # noqa

    def str_list(str_elem, xs):  # type: (Callable[[_T], Text], Sequence[_T]) -> Text
        return '[' + ', '.join(map(str_elem, xs)) + ']'

    # for now, this logic should continue to work as long as we are running on a proto3
    # implementation. If/when we switch to proto3, we will need to use attr.type

    # To support printing subgraphs, if we find a graph attribute, print out
    # its name here and pass the graph itself up to the caller for later
    # printing.
    graphs = []
    if attr.HasField("f"):
        content.append(str_float(attr.f))
    elif attr.HasField("i"):
        content.append(str_int(attr.i))
    elif attr.HasField("s"):
        # TODO: Bit nervous about Python 2 / Python 3 determinism implications
        content.append(repr(_sanitize_str(attr.s)))
    elif attr.HasField("t"):
        if len(attr.t.dims) > 0:
            content.append("<Tensor>")
        else:
            # special case to print scalars
            field = STORAGE_TENSOR_TYPE_TO_FIELD[attr.t.data_type]
            content.append('<Scalar Tensor {}>'.format(str(getattr(attr.t, field))))
    elif attr.HasField("g"):
        content.append("<graph {}>".format(attr.g.name))
        graphs.append(attr.g)
    elif attr.floats:
        content.append(str_list(str_float, attr.floats))
    elif attr.ints:
        content.append(str_list(str_int, attr.ints))
    elif attr.strings:
        # TODO: Bit nervous about Python 2 / Python 3 determinism implications
        content.append(str(list(map(_sanitize_str, attr.strings))))
    elif attr.tensors:
        content.append("[<Tensor>, ...]")
    elif attr.graphs:
        content.append('[')
        for i, g in enumerate(attr.graphs):
            comma = ',' if i != len(attr.graphs) - 1 else ''
            content.append('<graph {}>{}'.format(g.name, comma))
        content.append(']')
        graphs.extend(attr.graphs)
    else:
        content.append("<Unknown>")
    if subgraphs:
        return ' '.join(content), graphs
    else:
        return ' '.join(content)

def printable_graph(graph, prefix=''):  # type: (GraphProto, Text) -> Text
    content = []
    indent = prefix + '  '
    # header
    header = ['graph', graph.name]
    initializers = {t.name for t in graph.initializer}
    if len(graph.input):
        header.append("(")
        in_strs = []  # required inputs
        in_with_init_strs = []  # optional inputs with initializer providing default value
        for inp in graph.input:
            if inp.name not in initializers:
                in_strs.append(printable_value_info(inp))
            else:
                in_with_init_strs.append(printable_value_info(inp))
        if in_strs:
            content.append(prefix + ' '.join(header))
            header = []
            for line in in_strs:
                content.append(prefix + '  ' + line)
        header.append(")")

        if in_with_init_strs:
            header.append("optional inputs with matching initializers (")
            content.append(prefix + ' '.join(header))
            header = []
            for line in in_with_init_strs:
                content.append(prefix + '  ' + line)
            header.append(")")

        # from IR 4 onwards an initializer is not required to have a matching graph input
        # so output the name, type and shape of those as well
        if len(in_with_init_strs) < len(initializers):
            graph_inputs = {i.name for i in graph.input}
            init_strs = [printable_tensor_proto(i) for i in graph.initializer
                         if i.name not in graph_inputs]
            header.append("initializers (")
            content.append(prefix + ' '.join(header))
            header = []
            for line in init_strs:
                content.append(prefix + '  ' + line)
            header.append(")")

    header.append('{')
    content.append(prefix + ' '.join(header))
    graphs = []  # type: List[GraphProto]
    # body
    for node in graph.node:
        pn, gs = printable_node(node, indent, subgraphs=True)
        assert isinstance(gs, list)
        content.append(pn)
        graphs.extend(gs)
    # tail
    tail = ['return']
    if len(graph.output):
        tail.append(
            ', '.join(['%{}'.format(out.name) for out in graph.output]))
    content.append(indent + ' '.join(tail))
    # closing bracket
    content.append(prefix + '}')
    for g in graphs:
        content.append('\n' + printable_graph(g))
    return '\n'.join(content)

pg = printable_graph(model.graph, '')
print pg
