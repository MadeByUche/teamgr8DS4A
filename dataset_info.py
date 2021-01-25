# Data schemas and other dataset information
from dataclasses import dataclass
from dataframe_transformation_helpers import (
    clean_x_out_of_n,
    filter_out_rows_with_cols_all_nans,
    scrub_special_chars_from_column_values,
    categorize_columns,
    hcahps_hospital_widen
)
import pandera as pa
from pandera import Column, DataFrameSchema
from typing import List, Dict, Optional, Tuple
import copy

file_with_point_locations = [
    "hospital_general_information",
    "patient_experience_care_domain_scores",
    "hospital_hchaps",
    "hospital_value_based_performance"
]
POINT_LOCATION_COL = "location"

DEFAULT_GEOCODE_COLS = ["address", "city", "state", "zip_code"]

BASE_COL_SCHEMA_ARGS = {
    "coerce": True,
    "nullable": True
}

BASE_CMS_SCHEMA = {
    "facility_id": Column(pa.String, **BASE_COL_SCHEMA_ARGS),
    "facility_name": Column(pa.String, **BASE_COL_SCHEMA_ARGS),
    "address": Column(pa.String, **BASE_COL_SCHEMA_ARGS),
    "city": Column(pa.String, **BASE_COL_SCHEMA_ARGS),
    "state": Column(pa.String, **BASE_COL_SCHEMA_ARGS),
    "zip_code": Column(pa.String, **BASE_COL_SCHEMA_ARGS),
    "county_name": Column(pa.String, **BASE_COL_SCHEMA_ARGS)
}


def add_base_cms_schema(schema):
    s = copy.deepcopy(BASE_CMS_SCHEMA)
    s.update(schema)
    return DataFrameSchema(s)


@dataclass
class BaseDataInfo:
    schema: DataFrameSchema
    data_columns: Optional[Tuple[str]] = ()
    data_columns_search_key: Optional[Tuple[str]] = ()


def wrapped_categorize_columns(df, data_info):
    return categorize_columns(
        df,
        column_category_map=data_info.data_column_category_map,
        column_search_key_category_map=data_info.data_column_search_key_category_map
    )


def wrapped_hcahps_hospital_widen(df):
    t_df, measure_id_map, new_expanded_columns = hcahps_hospital_widen(df)
    return t_df


DATA_TRANSFORMATION_FUNCTION_MAP = {
    "data_column_category_map": wrapped_categorize_columns,
    "data_column_search_key_category_map": wrapped_categorize_columns,
    # For this member we can simply run the functions that are available
    # NOTE(anewla): we expect that these transform functions will update the dataframe and return the updated
    # dataframe
    "data_transformation_functions": None,
}

@dataclass
class DataTransformationInfo:
    data_column_category_map: Optional[Dict[str, List[str]]] = None
    data_column_search_key_category_map: Optional[Dict[str, List[str]]] = None
    # List of functions that should be executed post data cleaning, but pre typing
    # NOTE(anewla): we expect data cleaning to include all the basic essentials for preparing the dataset for further
    # transformations. This member will contain
    data_transformation_functions: Optional[List[callable]] = None

    @classmethod
    def transformation_keys(cls):
        return [k for k in cls.__dict__ if "__" not in k and "transformation_keys" not in k]



@dataclass
class DataInfo(DataTransformationInfo, BaseDataInfo):
    pass

@dataclass
class CMSHospitalCompareDataInfo(DataTransformationInfo, BaseDataInfo):
    # for datasets that follow hospital compare guidelines
    # we clean rows based on foonotes that are used
    clean_row_by_footnote: bool = True
    # NOTE(anewla): this is currenlty not in use
    footnote_expansion_needed: bool = False
    point_location_column: Optional[str] = None

hospital_general_information_info = CMSHospitalCompareDataInfo(
    schema=add_base_cms_schema({
        "phone_number": Column(pa.String, **BASE_COL_SCHEMA_ARGS),
        "hospital_type": Column(pa.String, **BASE_COL_SCHEMA_ARGS),
        "hospital_ownership": Column(pa.String, **BASE_COL_SCHEMA_ARGS),
        "emergency_services": Column(pa.String, **BASE_COL_SCHEMA_ARGS),
        "meets_criteria_for_promoting_interoperability_of_ehrs": Column(pa.String, **BASE_COL_SCHEMA_ARGS),
        "hospital_overall_rating": Column(pa.Float, **BASE_COL_SCHEMA_ARGS),
        "hospital_overall_rating_footnote": Column(pa.Int, nullable=True),
        ".*_comparison_footnote$": Column(pa.Float, **BASE_COL_SCHEMA_ARGS, regex=True),
        ".*_comparison$": Column(pa.Category, **BASE_COL_SCHEMA_ARGS, regex=True),
        "lat": Column(pa.Float, **BASE_COL_SCHEMA_ARGS),
        "lng": Column(pa.Float, **BASE_COL_SCHEMA_ARGS)
    }),
    data_columns_search_key=(".*_rating$", ".*_comparison$"),
    point_location_column=POINT_LOCATION_COL,
    data_column_search_key_category_map={
        ".*_comparison$": [
            "Below the national average",
            "Same as the national average",
            "Above the national average",
        ]
    }
)

patient_experience_care_domain_scores_info = CMSHospitalCompareDataInfo(
    schema=add_base_cms_schema({
        ".*_points$": Column(pa.Float, **BASE_COL_SCHEMA_ARGS, regex=True),
        ".*_threshold$": Column(pa.Float, **BASE_COL_SCHEMA_ARGS, regex=True),
        ".*_rate$": Column(pa.Float, **BASE_COL_SCHEMA_ARGS, regex=True),
        ".*_benchmark$": Column(pa.Float, **BASE_COL_SCHEMA_ARGS, regex=True),
        ".*_floor$": Column(pa.Float, **BASE_COL_SCHEMA_ARGS, regex=True),
        ".*_score$": Column(pa.Float, **BASE_COL_SCHEMA_ARGS, regex=True),
        "lat": Column(pa.Float, **BASE_COL_SCHEMA_ARGS),
        "lng": Column(pa.Float, **BASE_COL_SCHEMA_ARGS),
    }),
    data_columns_search_key=(".*_points$", ".*_threshold$", ".*_rate$", ".*_benchmark$", ".*_dimension_score$",
                             ".*_floor$",
                             ".*_score$"),
    point_location_column=POINT_LOCATION_COL,
    data_transformation_functions=[
        lambda df: clean_x_out_of_n(df, column_search_key=".*_points$"),
        lambda df: clean_x_out_of_n(
            df,
            column_search_key=".*_score$",
            column_search_block_keys=["hcahps_base_score", "hcahps_consistency_score"]
        )
    ]
)

complications_and_deaths_data_columns = (
    "compared_to_national", "denominator", "score", "lower_estimate", "higher_estimate"
)

complications_and_deaths_info = CMSHospitalCompareDataInfo(
    schema=add_base_cms_schema({
        "phone_number": Column(pa.String, **BASE_COL_SCHEMA_ARGS),
        "measure_id": Column(pa.String, **BASE_COL_SCHEMA_ARGS),
        "measure_name": Column(pa.String, **BASE_COL_SCHEMA_ARGS),
        "compared_to_national": Column(pa.Category, **BASE_COL_SCHEMA_ARGS),
        "denominator": Column(pa.Float, **BASE_COL_SCHEMA_ARGS),
        "score": Column(pa.Float, **BASE_COL_SCHEMA_ARGS),
        ".*_estimate$": Column(pa.Float, **BASE_COL_SCHEMA_ARGS, regex=True),
        "footnote": Column(pa.Float, **BASE_COL_SCHEMA_ARGS),
        "start_date": Column(pa.DateTime, **BASE_COL_SCHEMA_ARGS),
        "end_date": Column(pa.DateTime, **BASE_COL_SCHEMA_ARGS),

    }),
    data_columns=complications_and_deaths_data_columns,
    data_column_category_map={
        "compared_to_national": [
            "Number of Cases Too Small",
            "Worse Than the National Rate",
            "Worse Than the National Value",
            "No Different Than the National Rate",
            "No Different Than the National Value",
            "Better Than the National Rate",
            "Better Than the National Value"
        ]
    },
    data_transformation_functions=[
        lambda df: filter_out_rows_with_cols_all_nans(df, complications_and_deaths_data_columns)
    ]

)

# hospital_hchaps
hospital_hchaps_info = CMSHospitalCompareDataInfo(
    schema=add_base_cms_schema({
        "phone_number": Column(pa.String, **BASE_COL_SCHEMA_ARGS),
        "survey_response_rate_percent": Column(pa.Float, **BASE_COL_SCHEMA_ARGS),
        "start_date": Column(pa.DateTime, **BASE_COL_SCHEMA_ARGS),
        "end_date": Column(pa.DateTime, **BASE_COL_SCHEMA_ARGS),
        "lng": Column(pa.Float, **BASE_COL_SCHEMA_ARGS),
        "lat": Column(pa.Float, **BASE_COL_SCHEMA_ARGS),
        "measure_id_*": Column(pa.Float, **BASE_COL_SCHEMA_ARGS, regex=True),
        ".*_footnote$": Column(pa.String, **BASE_COL_SCHEMA_ARGS, regex=True)
    }),
    footnote_expansion_needed=True,
    data_columns_search_key=[".*_rating$", ".*_score$"],
    point_location_column=POINT_LOCATION_COL,
    data_transformation_functions=[wrapped_hcahps_hospital_widen]
)

# timely_effective_care_hospital
timely_effective_care_hospital_info = CMSHospitalCompareDataInfo(
    schema=add_base_cms_schema({
        "phone_number": Column(pa.String, **BASE_COL_SCHEMA_ARGS),
        "condition": Column(pa.String, **BASE_COL_SCHEMA_ARGS),
        "measure_id": Column(pa.String, **BASE_COL_SCHEMA_ARGS),
        "measure_name": Column(pa.String, **BASE_COL_SCHEMA_ARGS),
        "score": Column(pa.Float, **BASE_COL_SCHEMA_ARGS),
        "sample": Column(pa.Float, **BASE_COL_SCHEMA_ARGS),
        "footnote": Column(pa.String, **BASE_COL_SCHEMA_ARGS),
        "start_date": Column(pa.DateTime, **BASE_COL_SCHEMA_ARGS),
        "end_date": Column(pa.DateTime, **BASE_COL_SCHEMA_ARGS),

    }),
    data_columns=("score", "sample")
)

# hospital_value_based_performance
hospital_value_based_performance_info = CMSHospitalCompareDataInfo(
    schema=add_base_cms_schema({
        ".*_domain_score$": Column(pa.Float, **BASE_COL_SCHEMA_ARGS, regex=True),
        "total_performance_score": Column(pa.Float, **BASE_COL_SCHEMA_ARGS),
        "lat": Column(pa.Float, **BASE_COL_SCHEMA_ARGS),
        "lng": Column(pa.Float, **BASE_COL_SCHEMA_ARGS)
    }),
    data_columns_search_key=[".*score$"],
    point_location_column=POINT_LOCATION_COL,
    data_transformation_functions=[
        # NOTE(emmy): we found one facility_id: 330201 that had parentheses in it"s values for the following columns
        lambda df: scrub_special_chars_from_column_values(
            df,
            [
                "unweighted_normalized_clinical_outcomes_domain_score",
                "weighted_normalized_clinical_outcomes_domain_score",
                "total_performance_score"
            ]
        )
    ]
)

# TODO(anewla): fill out using emmy's cleanup code as a base
# us_city_population_estimates
# us_city_population_estimates = DataInfo(
#     schema=add_base_cms_schema({
#         ".*_domain_score$": Column(pa.Float, **BASE_COL_SCHEMA_ARGS, regex=True),
#         "total_performance_score": Column(pa.Float, **BASE_COL_SCHEMA_ARGS),
#         "lat": Column(pa.Float, **BASE_COL_SCHEMA_ARGS),
#         "lng": Column(pa.Float, **BASE_COL_SCHEMA_ARGS)
#     }),
#     data_columns_search_key=[".*score$"],
#     point_location_column=POINT_LOCATION_COL,
#     data_transformation_functions=[
#         # NOTE(emmy): we found one facility_id: 330201 that had parentheses in it"s values for the following columns
#         lambda df: scrub_special_chars_from_column_values(
#             df,
#             [
#                 "unweighted_normalized_clinical_outcomes_domain_score",
#                 "weighted_normalized_clinical_outcomes_domain_score",
#                 "total_performance_score"
#             ]
#         )
#     ]
# )
