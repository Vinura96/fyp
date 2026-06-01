import time
import random


def merge(left,right): #merges 2 sorted lists together

    result = []
    i, j = 0, 0

    #Goes through both lists
    while i < len(left) and j < len(right):
    #Adds smaller element of the lists to the final list
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result += left[i:]
    result += right[j:]

    return result

def mergesort(lst):

    #if there's only 1 element, no need to sort
    if len(lst) < 2:
        return lst
    #breaks down list into 2 halves
    middle = int(len(lst) / 2)

    #recursively splits and sorts each half
    left = mergesort(lst[:middle])
    right = mergesort(lst[middle:])

    #merges both sorted lists together
    return merge(left, right)
