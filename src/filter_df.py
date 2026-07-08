


def filter_df(current_df, filter_criteria, function):
    return current_df[filter_criteria].apply(function)


