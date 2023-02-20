import random

from shamir.generator.constants import NOUNS, ADJECTIVES

def get_id():
    noun = random.choice(NOUNS)
    adjective = random.choice(ADJECTIVES)
    number = str(random.randrange(1, 9999)).zfill(4)
    return f"{number}-{adjective}-{noun}"
