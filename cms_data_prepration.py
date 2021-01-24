from dataframe_transformation_helpers import filter_out_rows_with_cols_all_nans, create_lat_long_from_point, \
    geocode_and_update_lat_lng, \
    format_zip_code, replace_with_nan, LAT_LNG_COL_NAMES, clean_columns
from dataset_info import BaseDataInfo, DataTransformationInfo, DATA_TRANSFORMATION_FUNCTION_MAP, \
    CMSHospitalCompareDataInfo
from cms_hospital_compare_footnote_data_dictionary import CMS_HOSPITAL_COMPARE_FOOTNOTE_DATA_DICT, POOR_SAMPLE_KEY
import pandera as pa
import re
import numpy as np


def clean_nans(
        df,
        data_columns=None,
        filter_all_nan_data_rows=False,
        nan_replacement_lst=None,
        nan_replacement_str_key_lst=None,
        **kwargs
):
    """
    data_columns: columns that have valuable data in them, and should be cleaned with extra care
    filter_all_nan_rows: in combination with data_columns, finds rows that have at least 1 non np.nan value
    nan_replacement_lst: values that should be replaced with np.nan (only checks data columns)
    nan_replacement_str_prefix_lst: prefix for str values that should be replaced with np.nan (only checks data columns)
    """
    replace_with_nan(
        df,
        data_columns,
        replacement_lst=nan_replacement_lst,
        replacement_str_key_lst=nan_replacement_str_key_lst
    )

    if filter_all_nan_data_rows:
        return filter_out_rows_with_cols_all_nans(df, data_columns)
    return df


def clean_locations(
        df,
        source_lat_lng_column=None,
        lat_lng_columns=LAT_LNG_COL_NAMES,
        geocode_cols=[],
        geocode_condition_func=None,
        **kwargs
):
    if source_lat_lng_column is None and not geocode_cols:
        return df

    if source_lat_lng_column is not None:

        sample_df = df.loc[
            df[source_lat_lng_column].notnull(), source_lat_lng_column
        ]
        if "point" in sample_df.iloc[0].lower():
            df = create_lat_long_from_point(df, source_lat_lng_column)
        else:
            raise NotImplementedError(
                f"Unknown location type in {df.name} column: {source_lat_lng_column}\n"
                f"sample: {sample_df.sample(10)}"
            )
    if geocode_cols:
        # since geocode_cols is not empty we will attempt to geocode any columns
        # that haven't been
        if geocode_condition_func is not None:
            # to filter and operrate only rows that need this functionality
            # TODO(anewla): fill in this code based on the criteria for which we
            # we choose rows to be geo coded
            raise NotImplementedError()
        df = geocode_and_update_lat_lng(df, geocode_cols, lat_lng_columns=lat_lng_columns)
        pass

    return df


def nan_data_column_by_footnote(df):
    # Walks through footnote columns using mappings dict and replaces any data source in the source column
    # with nan. (source column is the column for which the footnote column is responsible for)
    footnote_columns = [c for c in df.columns if re.search("footnote", c) is not None]
    columns_with_footnotes = {
        footnote_column.split("_footnote")[0]: footnote_column
        for footnote_column in footnote_columns
    }
    # NOTE(anewla): for sake of convenience, we will store footnotes both as integers and floats wrapped as strings
    # to ensure we capture any and all footnotes in the dataset
    bad_sample_footnotes = []
    for k, v in CMS_HOSPITAL_COMPARE_FOOTNOTE_DATA_DICT.items():
        if v.get(POOR_SAMPLE_KEY, False):
            bad_sample_footnotes.extend([str(k), str(float(k))])
    if bad_sample_footnotes:
        # NOTE(anewla): this code could be used to completely filter out any rows that have a column with a poor sampling footnote
        # rows_with_bad_footnotes = eval(" | ".join(
        #         [
        #             f"(df['{c}'].astype(str).str.split(', ').apply(lambda x: len({bad_sample_footnotes_set}.intersection(x)) > 0))"
        #             for c in footnote_columns
        #         ]
        #      )
        # )
        # return df[~rows_with_bad_footnotes]
        bad_sample_footnotes_set = set(bad_sample_footnotes)
        for data_column, footnote_column in columns_with_footnotes.items():
            df.loc[
                df[footnote_column].astype(str).str.split(',').apply(
                    lambda x: len(set(bad_sample_footnotes).intersection(x)) > 0
                ),
                data_column
            ] = np.nan
    return df


def row_diff_msg(row_count_pre_clean, row_count_post_clean, msg_prefix):
    print(
        f"{msg_prefix} -> REMOVED: {row_count_post_clean} rows "
        f"{round((row_count_post_clean - row_count_pre_clean) / row_count_pre_clean, 2) * 100}% of the data"
    )


def clean_dataset(df, name, data_info: BaseDataInfo, **kwargs):
    msg_prefix = f"CLEANING: {name}"
    print(msg_prefix)
    rtn_df = df.copy()
    rtn_df.name = name

    print(f"{msg_prefix} --> clean_columns")
    rtn_df = clean_columns(rtn_df)

    print(f"{msg_prefix} --> format_zip_code")
    rtn_df = format_zip_code(rtn_df)

    clean_footnotes_msg = f"{msg_prefix} --> clean_footnotes"
    print(clean_footnotes_msg)
    if isinstance(data_info, CMSHospitalCompareDataInfo):
        row_count_pre_clean = rtn_df.shape[0]
        rtn_df = nan_data_column_by_footnote(rtn_df)
        row_count_post_clean = rtn_df.shape[0]
        row_diff_msg(row_count_pre_clean, row_count_post_clean, clean_footnotes_msg)

    clean_nans_msg = f"{msg_prefix} --> clean_nans"
    print(clean_nans_msg)
    row_count_pre_clean = rtn_df.shape[0]
    rtn_df = clean_nans(rtn_df, **kwargs)
    row_count_post_clean = rtn_df.shape[0]
    row_diff_msg(row_count_pre_clean, row_count_post_clean, clean_nans_msg)

    # NOTE(anewla): we are actually cleaning through all values, if we find that this is causing issues we can isolate
    # to the columns of interest through the following
    # nan_replacement_lst = data_info.data_columns
    # nan_replacement_str_key_lst = data_info.data_columns_search_key

    print(f"{msg_prefix} --> clean_locations")
    rtn_df = clean_locations(rtn_df, source_lat_lng_column=data_info.point_location_column, **kwargs)

    print(f"{msg_prefix} - COMPLETE")
    return rtn_df


def prepare_and_transform_dataset(df, name, data_info: BaseDataInfo, **kwargs):
    rtn_df = df.copy()
    # TODO(anewla): remove debugging code once the pipeline is finalized
    skip_transform_list = []
    skip_validate_list = ["timely_effective_care_hospital"]
    if name not in skip_transform_list and isinstance(data_info, DataTransformationInfo):
        for k in DataTransformationInfo.transformation_keys():
            curr_transform_info = data_info.__getattribute__(k)
            if curr_transform_info is not None:
                func = DATA_TRANSFORMATION_FUNCTION_MAP[k]
                if func is not None:
                    rtn_df = func(rtn_df, data_info)
                    assert rtn_df is not None
                elif k == "data_transformation_functions" and curr_transform_info:
                    for transform_func in curr_transform_info:
                        rtn_df = transform_func(rtn_df)
                        assert rtn_df is not None
    assert rtn_df is not None
    try:
        if name not in skip_validate_list:
            data_info.schema.validate(rtn_df, inplace=True)
    except pa.errors.SchemaError as e:
        str_e = str(e)
        coercing_issue = "Error while coercing"
        col_missing = "not in dataframe"
        if coercing_issue in str_e:
            msg = "Sample of column with exception. col:"
            col = str_e[len(coercing_issue):].split("'")[1]
            schema_column = data_info.schema.columns[col]
            if schema_column.regex:
                msg = f"Column is regex: {col}, example col:"
                col = [c for c in rtn_df.columns if re.search(col, c) is not None][0]

            raise Exception(f"{msg} {col} {rtn_df[col].sample(100).to_string}\n{e}")
        elif col_missing in str_e:
            col = str_e[len("column "):].split("'")[1]
            raise Exception(f"Missing column: {col}\nAll Columns: {rtn_df.columns}\n{e}")

        else:
            raise Exception(e)

    print(f"DATA PREPERATION {name} - COMPLETE")
    rtn_df.name = name
    return rtn_df


def clean_and_prepare_dataset(df, name, data_info: BaseDataInfo, **kwargs):
    rtn_df = df.copy()
    rtn_df.name = name
    rtn_df = clean_dataset(rtn_df, name, data_info, **kwargs)
    rtn_df = prepare_and_transform_dataset(rtn_df, name, data_info, **kwargs)

    return rtn_df
