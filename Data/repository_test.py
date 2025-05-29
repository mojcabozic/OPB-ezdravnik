from repository import Repo
from models import *

# V tej datoteki lahko testiramo funkcionalnost repozitorija,
# brez da zaganjamo celoten projekt.

repo = Repo()
# Dobimo vse zdravnike
zdravniki = repo.dobi_zdravnike()


# jih izpišemo
for z in zdravniki:
    print(z)

# Dobimo vse oddelke
oddelki = repo.dobi_oddelke()
for o in oddelki:
    print(z)


