def merge_sort(list_to_sort,front,rear):
    if front < rear:
        middle = ((front + rear) // 2)
        List_Left = merge_sort(list_to_sort,front,middle)
        List_Right = merge_sort(list_to_sort, middle + 1, rear)
        return merge(List_Left, List_Right)
    else:
        return [list_to_sort[front]]

def merge(List_Left,List_Right):
    l = []
    while len(List_Left) > 0 and len(List_Right) > 0:
        if List_Left[0] > List_Right[0]:
            l.append(List_Right[0])
            del List_Right[0]
            #remove first item from List Right
        else:
            l.append(List_Left[0])
            del List_Left[0]
            #remove first itme from List Left
    while len(List_Left) > 0:
        l.append(List_Left[0])
        del List_Left[0]
        #remove first itme from List Left
    while len(List_Right) > 0:
        l.append(List_Right[0])
        del List_Right[0]
        #remove first item from List Right
    return l
