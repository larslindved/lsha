from sandbox.EventHardcoded import event_func

#curr and prev are entire data rows
def is_chg_pt(curr, prev):

    chg_flag, _ = event_func(curr, prev)

    return chg_flag
