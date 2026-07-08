from get_gender_data import get_founder_gender

def rescue_unknowns(df, founder_col, gender_col):
    """Re-process only rows where gender is unknown or contains unknown."""
    mask = df[gender_col].apply(lambda x: 'unknown' in str(x).lower() if x is not None else True)
    unknown_count = mask.sum()

    if unknown_count == 0:
        print(f"No unknowns found in {gender_col}.")
        return df

    print(f"Attempting to rescue {unknown_count} unknowns in {gender_col}...")

    # Targeted update
    df.loc[mask, gender_col] = df.loc[mask, founder_col].apply(lambda x: get_founder_gender(x, use_web_search=True))

    new_unknown_count = df[gender_col].apply(lambda x: 'unknown' in str(x).lower()).sum()
    print(f"Resolution complete. Unknowns remaining: {new_unknown_count} (Rescued {unknown_count - new_unknown_count})")
    return df