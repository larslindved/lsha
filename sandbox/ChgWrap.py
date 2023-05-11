from sandbox.EventFunc import event_func
# from sandbox.EventHardcoded import event_func

def is_chg_pt(curr, prev):
    chg_flag, _te = event_func(curr, prev)
    return chg_flag
