import time
import onnx, onnx.numpy_helper
import numpy as np
model = onnx.load("model.onnx")
f= open("nodes.txt","w+")
for t in model.graph.node:
    f.write(str(t.output))
    print t.output
    print "aaaaaaaaaaaaaaaaaaaaa"
    print t.attribute
    print "bbbbbbbbbbbbbbbbbbbbb"
    f.write(str(t.attribute))

f.close()
