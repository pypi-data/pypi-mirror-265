from inspect import getmembers, isfunction

def askFor(question, validator, error=lambda: None, required=True, final=None):
    out = input(question)
    if required:
        while not validator(out):
            error()
            out = input(question)
    if not validator(out):
        error()
        out = final or input(question)
    return out


def askForSec(*args):
    try:
        return askFor(*args)
    except KeyboardInterrupt:
        raise KeyboardInterrupt()
    except:
        return askForSec(*args)


def imports(module):
    for val in getmembers(module, isfunction):
        yield val
