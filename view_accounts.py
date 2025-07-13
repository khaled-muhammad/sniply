import os

from utils import getSMAPath

smaPath = getSMAPath()

def viewAccounts():
    for smp in [i for i in os.listdir(smaPath) if not i.startswith('.')]:
        print(f"- {smp.capitalize()}: ")
        for acc in [i for i in os.listdir(os.path.join(smaPath, smp)) if not i.startswith('.')]:
            print(f"    - {acc}")