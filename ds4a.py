"""
High level todo
    DATA ISSUES
        hospital_hchaps
            need to expand footnotes
        timely_effective_care_hospital
            need to expand footnotes
            score -> has 'HIGH' instead of an integer there....

    -> Analysis
        https://towardsdatascience.com/eveything-you-need-to-know-about-interpreting-correlations-2c485841c0b8

    -> CLEANING UPDATES
        -> categorical variables -> indicator variables (pd.get_dummies)
        -> writing shouldn't have index
        -> cleaning rows that have footnotes (using data dictionary)
            #16 = Not Available
            #19 = Not Available
            #17 = The hospital star rating only based on inpatient services
            #5 = Not Available
            #22 = Not Available
            #23 = The data is based on claims from the hospital
    -> Future work
        -> need some refresh pipeline....



    BEFORE SATURDAY

    -> Team Meeting
        SATURDAY
        -> agreeing on the footnotes that we should filter out
            for hchahp need to verify how this transformation is actually impacting
            data in relationship to mapping
        -> Setting up pipeline to run through everything
        -> each data owner should walk through and inspect their respective output dataset
        -> taking stock of tasks for what needs to be done on saturday
            -> infrastructure: lead point andre
            -> ...?
    -> brainstorming EDA and joining process


"""
# TODO(anewla):

file_map = {
    "hospital_general_information":
        "Hospital_General_Information.csv",
    "patient_experience_care_domain_scores":
        "Hospital_Value-Based_Purchasing__HVBP____Patient_Experience_of_Care_Domain_Scores__HCAHPS_.csv",
    "complications_and_deaths":
        "complications&deaths.csv",
        # 'compared_to_national', 'denominator', 'score', 'lower_estimate',
       # 'higher_estimate'
    "hospital_hchaps":
        "patient_survey__hcahps_hospital.csv",
    "timely_effective_care_hospital":
        "Timely_and_Effective_Care_-_Hospital.csv",
    "hospital_value_based_performance":
        "Hospital_Value-Based_Purchasing__HVBP____Total_Performance_Score.csv",
}

