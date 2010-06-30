# FIXME: fatal, cannot be used
def __merge_two_dict(d1,d2):
    for key in d2.keys():
        d1[key] = d2[key]
    return d1

def merge_dict(d1,*d2):
    src = d1.copy()
    for d in d2:
        src = __merge_two_dict(src,d)