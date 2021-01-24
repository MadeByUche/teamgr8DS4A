"""
WORK
    -> generating clean prod output
        -> categorical data as dummies (certain measures in timely and effective care as well as complications and deths)
        -> cleaning pipeline: us_city_population_estimates
    -> adding analysis pipeline functionality
        -> dataset generation
            -> generating merged dataset that was used for phase 1 analysis
            -> generating merged datasetst that were used for phase 2 analysis
                -> hospital with population data
                -> timely and effective care + complications and deaths need expanded output

        -> OLS linear models
        -> ttests to assess the mean and whether or not there is a any signficant difference
        -> anova to assess the difference between two or more catergories
        -> anova on linear model: to assess the variance in the model
    -> Additional analysis
        -> what is the distribution of foot notes for hospital compare datasets
            -> is this an indicator of a general trend in data collection for hospitals
    -> transfer documentation that was used for cleaning pipeline deliverable


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

