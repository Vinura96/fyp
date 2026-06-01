import time
import onnx, onnx.numpy_helper
import numpy as np
f= open("dataa.txt","w+")
model = onnx.load("model.onnx")
i = 0
for t in model.graph.initializer:
    k = onnx.numpy_helper.to_array(t)
    if(i==16):
        print(k)
    print type(k)
    print t.name
    print t.dims
    print t.data_type
    i = i + 1

f.close()
#[tensor] = [t for t in model.graph.initializer]
#w = numpy_helper.to_array(tensor)

#weights = model.graph.initializer
#print weights

#if (i==11):
        #k = onnx.numpy_helper.to_array(t)
        
        #print k
        #for s in range(len(k)):
            #print k[s]
        #f.write(str(t))
