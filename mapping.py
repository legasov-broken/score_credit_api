from lib import *

source = open('./WOE_dict_sorted.json')
source = json.load(source)

def dict_mapping(value):
    out_ = {}

    for ele_in in source:
        out_[ele_in] = None
        for ele_out in value:
            if ele_in == ele_out:
                print(value[ele_out])
                out_[ele_in] = value[ele_out] 
    return out_
