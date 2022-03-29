import random



def generate_verb():

      action = random.choice(["eat", "sleep", "fuck"])
      return action

def alice(a, b = None):
    return 'I like {}, lets do it'.format(a + "ing")