from lib import *
from score_all_users import score_users

# in
source_ = open('./input.json')
source = json.load(source_)

# out
 
print(score_users(source))












