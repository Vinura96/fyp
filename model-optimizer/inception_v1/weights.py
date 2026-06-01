import time
import onnx, onnx.numpy_helper
import numpy as np
f= open("data.txt","w+")
model = onnx.load("model.onnx")
i = 0
for t in model.graph.initializer:
    if (i==2):
        k = onnx.numpy_helper.to_array(t)
        print type(k)
        print k
        for s in range(len(k)):
            print k[s]
        f.write(str(t))
    i = i + 1

f.close()
#[tensor] = [t for t in model.graph.initializer]
#w = numpy_helper.to_array(tensor)

#weights = model.graph.initializer
#print weights
