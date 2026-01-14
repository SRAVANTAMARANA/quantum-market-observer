def target_from_balance(df):
    return (df.high.max() + df.low.min()) / 2
