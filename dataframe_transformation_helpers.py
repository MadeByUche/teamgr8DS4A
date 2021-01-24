from geopy.geocoders import Nominatim
import pandas as pd
import re
import numpy as np

LAT_LNG_COL_NAMES = ['lat', 'lng']
GEO_COORD_COLUMN_NAME = "lat_lng"
POINT_TO_LAT_LNG_COL_NAMES = ['lng', 'lat']
# point column normally has values of type: POINT (-121.77291599999998 37.246742)
# oddly enough it is described in lng, lat instead of lat,lng, so we flip
SP_CHARS_LST = "!,@,#,$,%,^,&,\(,\),\*,-".split(",")


def clean_zip_code_column(df):
    zip_code_like_column = [c for c in df.columns if "zip" in c]

    if len(zip_code_like_column) > 1:
        raise NotImplementedError(
            f"{df.name} has the "
            f"following zip like columns: {zip_code_like_column}"
        )
    elif zip_code_like_column:
        # cleaning up zip code column to be properly formatted
        if zip_code_like_column[0] != "zip_code":
            print(f"Renaming {df.name}.{zip_code_like_column[0]} to zip_code")
            df.rename(columns={zip_code_like_column[0]: "zip_code"}, inplace=True)
    return df


def format_zip_code(df, column="zip_code"):
    if column in df.columns:
        df[column] = df[column].astype(str).str.zfill(5)
    return df


# NOTE: used for creating full_address column, which aids in geocoding
def str_join_columns(df, ordered_columns, new_column, seperator=" "):
    def agg_func(row):
        ",".join([str(row[c]) for c in ordered_columns])

    df[new_column] = df[ordered_columns].agg(agg_func, axis=1)
    return df


def replace_with_nan(
        df,
        columns=None,
        replacement_lst=None,
        replacement_str_key_lst=None,
        inplace=True
):
    if columns is None:
        columns = df.columns

    if replacement_lst is None and replacement_str_key_lst is None:
        return df
    if replacement_lst:
        df.replace(replacement_lst, np.nan, inplace=inplace)
    if replacement_str_key_lst:

        def contains_lst(dataframe, column, lst):
            return dataframe[column].str.contains("|".join(lst))

        # NOTE(anewla): when setting up new datasets to clean we often find issues in this code.
        # I've changed the format from list comprehension to enable streamlined debugging
        to_replace_pairs = []
        for column in columns:
            if df[column].dtype == 'O' and contains_lst(df, column, replacement_str_key_lst).sum():
                to_replace_pairs.append(
                    (
                        column,
                        list(df.loc[
                                 contains_lst(df, column, replacement_str_key_lst).replace(np.nan, False),
                                 column
                             ].unique())
                    )
                )
        print(
            f"replace_with_nan: {df.name}, prefixes: {replacement_str_key_lst}"
            f", pairs: {to_replace_pairs}"
        )
        for column, unique_values in to_replace_pairs:
            df[column].replace(unique_values, np.nan, inplace=inplace)
    return df


def create_lat_long_from_point(df, point_column, new_coord_columns=POINT_TO_LAT_LNG_COL_NAMES, drop_point_column=True, add_geocoord=True):
    # clean Location column (remove characters, split into lat and long columns, and change to type float)
    df[point_column] = df[point_column].str.slice(start=7, stop=-1)
    df[new_coord_columns] = df[point_column].str.split(expand=True)
    if add_geocoord:
        df[GEO_COORD_COLUMN_NAME] = df[LAT_LNG_COL_NAMES[0]] + "," + df[LAT_LNG_COL_NAMES[1]]
    if drop_point_column:
        df.drop(columns=point_column, inplace=True)
    return df


def filter_out_rows_with_cols_all_nans(df, data_columns):
    some_data_map = eval(" | ".join([f"(df['{c}'].notnull())" for c in data_columns]))
    return df[some_data_map]

def drop_unneeded_columns(df, columns_to_drop):
    for c in columns_to_drop:
        if c in df.columns:
            df.drop(column=c, inplace=True)
    return df


def clean_columns(df):
    def gen_rename_column_dict(df):
        d = {}
        sp_chars_to_replace_with_underscore = [" ", ","]
        for c in df.columns:
            new_c = re.sub("|".join(SP_CHARS_LST), "", c).replace("\\", "").replace("\/", "")
            new_c = re.sub("|".join(sp_chars_to_replace_with_underscore), "_", new_c)
            d[c] = new_c.lower()
        return d

    df.rename(columns=gen_rename_column_dict(df), inplace=True)
    return df


# TODO(anewla): runtime of this code needs to be assessed. compare runtimes across team
def geocode_and_update_lat_lng(df, address_cols, lat_lng_columns=LAT_LNG_COL_NAMES, user_agent="Address Predictor",
                               timeout=5):
    geolocator = Nominatim(user_agent=user_agent, timeout=timeout)

    def custom_geocode(row):
        location = geolocator.geocode(" ".join(row[address_cols]))
        if location:
            location = ','.join([str(location.latitude), str(location.longitude)])
        else:
            location = ",".join([str(np.nan)] * 2)
        return location

    df[lat_lng_columns] = df.apply(lambda x: custom_geocode(x), axis=1).str.split(",", expand=True)
    return df


# patient_experience_care_domain_scores
def clean_x_out_of_n(df, column_search_key="points", column_search_block_keys=[]):
    # Values in columns with the prefix points, can be written as float values
    # currently they are of the form X out of 10
    columns_to_clean = [
        c
        for c in df.columns
        if c not in column_search_block_keys and re.search(column_search_key, c) is not None
    ]
    for c in columns_to_clean:
        df[c] = df[c].str.slice(0, 1)
    return df


def scrub_special_chars_from_column_values(df, columns):
    for c in columns:
        df[c] = df[c].str.replace("|".join(SP_CHARS_LST), "")
    return df


def categorize_columns(df, column_category_map=None, column_search_key_category_map=None):
    curr_column_category_map = {}
    if column_category_map is not None:
        curr_column_category_map.update(column_category_map)
    if column_search_key_category_map is not None:
        for search_key, categories in column_search_key_category_map.items():
            try:
                curr_columns_with_search_key = [c for c in df.columns if re.search(search_key, c) is not None]
            except Exception as e:
                raise Exception(f"search_key: {search_key}\n{e}")
            for c in curr_columns_with_search_key:
                curr_column_category_map[c] = categories

    for column, categories in curr_column_category_map.items():
        curr_additional_kwargs = {}
        if categories is not None:
            curr_additional_kwargs = {
                "ordered": True,
                "categories": categories
            }
        df[column] = pd.Categorical(
            df[column],
            **curr_additional_kwargs
        )

    return df


def find_non_numeric_values(df, column):
    # returns a list of the non numeric values found in df
    unique_values = df[column].unique()
    non_numeric = []
    for v in unique_values:
        if str(v) == str(np.nan):
            continue
        try:
            int(v)
        except:
            non_numeric.append(v)
    return non_numeric


def hcahps_hospital_widen(df):
    column_keys = [".*_rating$", ".*_score$", "hcahps_linear_mean_value"]
    columns_to_numeric = []
    for ck in column_keys:
        columns_to_numeric.extend([c for c in df.columns if re.search(ck, c) is not None])
    for c in columns_to_numeric:
        df[c] = df[c].astype("float64")

    patient_survey_rating_col_count = len(df[df['patient_survey_star_rating'].notnull()]['hcahps_measure_id'].unique())
    linear_mean_value_col_count = len(df[df['hcahps_linear_mean_value'].notnull()]['hcahps_measure_id'].unique())

    # we expand hcahps_measure_id into columns, using patient_survey_star_rating as value
    facility_id_hcahps_measure_id_cxtab_pssr = pd.crosstab(index=df['facility_id'], columns=df['hcahps_measure_id'],
                                                           values=df['patient_survey_star_rating'], aggfunc=lambda x: x)
    facility_id_hcahps_measure_id_cxtab_pssr.rename(
        columns={c: f"MEASURE_ID_{c}_PATIENT_SURVEY_STAR_RATING" for c in facility_id_hcahps_measure_id_cxtab_pssr.columns},
        inplace=True
    )
    # sanity check that we are getting the expected shape
    if facility_id_hcahps_measure_id_cxtab_pssr.shape[1] != patient_survey_rating_col_count:
        raise Exception(f"Issue with data shape expected {linear_mean_value_col_count} "
                        f"found: {facility_id_hcahps_measure_id_cxtab_pssr.shape[1]}")


    # we expand hcahps_measure_id into columns, using hcahps_linear_mean_value as value
    facility_id_hcahps_measure_id_cxtab_lmv = pd.crosstab(index=df['facility_id'], columns=df['hcahps_measure_id'],
                                                          values=df['hcahps_linear_mean_value'], aggfunc=lambda x: x)
    facility_id_hcahps_measure_id_cxtab_lmv.rename(
        columns={c: f"MEASURE_ID_{c}_LINEAR_MEAN_VALUE_{c}" for c in facility_id_hcahps_measure_id_cxtab_lmv.columns},
        inplace=True
    )
    # sanity check that we are getting the expected shape
    if facility_id_hcahps_measure_id_cxtab_lmv.shape[1] != linear_mean_value_col_count:
        raise Exception(f"Issue with data shape expected {linear_mean_value_col_count} "
                        f"found: {facility_id_hcahps_measure_id_cxtab_lmv.shape[1]}")


    new_expanded_columns = list(set(
        list(facility_id_hcahps_measure_id_cxtab_pssr.columns) + list(facility_id_hcahps_measure_id_cxtab_lmv.columns)))
    new_expanded_columns.sort()

    # joining against expanded pssr df
    expanded_pssr_df = df.join(facility_id_hcahps_measure_id_cxtab_pssr, on='facility_id')

    # joining against expanded lmv df
    transformed_df = expanded_pssr_df.join(facility_id_hcahps_measure_id_cxtab_lmv, on='facility_id').drop(
        [
            # Columns used for expansion
            'hcahps_measure_id',
            'patient_survey_star_rating',
            'hcahps_linear_mean_value',

            # Descriptive columns no longer needed after expansion
            'hcahps_question',
            'hcahps_answer_description',

            # Columns dropped indicating survey responses
            'hcahps_answer_percent',
            'number_of_completed_surveys',
        ],
        axis=1
    ).drop_duplicates()
    temp_group_by = df.groupby("hcahps_measure_id	hcahps_question	hcahps_answer_description".split("\t"))[
        'hcahps_measure_id'].count().index
    measure_id_map = {measure_id: {'question': question, 'description': description} for
                      measure_id, question, description in temp_group_by}
    transformed_df.rename(columns={c: c.lower() for c in transformed_df.columns}, inplace=True)
    return transformed_df, measure_id_map, new_expanded_columns
