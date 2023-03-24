def my_sort(iterable, key, reverse: bool):
    if reverse is False:
        for i in range(len(iterable)-1):
            if key(iterable[i]) > key(iterable[i+1]):
                iterable[i], iterable[i+1] = iterable[i+1], iterable[i]
    else:
        for i in range(len(iterable)-1):
            if key(iterable[i]) < key(iterable[i+1]):
                iterable[i], iterable[i+1] = iterable[i+1], iterable[i]
    return iterable
