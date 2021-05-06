# Standard library imports

# Third party imports
import pandas

# Local application/library specific imports
import queries


def dataframe_code_sets():
    """Gets and DataFrames all code sets into a dict with their labels as keys

    :return: a dict of code sets in dataframes {label: DataFrame}
    """
    cs = queries.get_code_sets()
    result = {}
    for key in cs['object'].keys():
        df_cs = pandas.DataFrame(data=queries.get_code_sets()['object'][key])
        df_cs = df_cs.set_index(df_cs.columns[0]).sort_index()
        result[key] = df_cs
    return result
