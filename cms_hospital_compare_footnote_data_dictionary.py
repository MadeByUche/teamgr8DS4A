POOR_SAMPLE_KEY = "is_poor_sample"
CMS_HOSPITAL_COMPARE_FOOTNOTE_DATA_DICT = {
  1: {
    "information": "The number of cases/patients is too few to report.  This footnote is applied:  • When the number of cases/patients does not meet the required  minimum amount for public reporting;  • When the number of cases/patients is too small to reliably tell  how well a hospital is performing; and/or  • To protect personal health information.",
    POOR_SAMPLE_KEY: True,
  },
  2: {
    "information": "Data submitted were based on a sample of cases/patients. This footnote indicates that a hospital chose to submit data for a random sample of its cases/patients while following specific rules for how to select the patients."
  },
  3: {
    "information": "Results are based on a shorter time period than required. This footnote indicates that the hospital’s results were based on data from less than the maximum possible time period generally used to collect data for a measure. View the Hospital Compare Data Collection Periods for more information. This footnote is applied: • When a hospital elected not to submit data for a measure for one or more, but not all possible quarters; • When there was no data to submit for a measure for one or more, but not all possible quarters; and/or • When a hospital did not successfully submit data for a measure for one or more, but not all possible quarters."
  },
  4: {
    "information": "Data suppressed by CMS for one or more quarters. The results for these measures were excluded for various reasons, such as data inaccuracies."
  },
  5: {
    "information": "Results are not available for this reporting period. This footnote is applied: • When a hospital elected not to submit data for the entire reporting period; or • When a hospital had no claims data for a particular measure; or • When a hospital elected to suppress a measure from being publicly reported.",
    POOR_SAMPLE_KEY: True,
  },
  6: {
    "information": "Fewer than 100 patients completed the HCAHPS survey. Use these scores with caution, as the number of surveys may be too low to reliably assess hospital performance. This footnote is applied when the number of completed surveys the hospital or its vendor provided to CMS is less than 100."
  },
  7: {
    "information": "No cases met the criteria for this measure. This footnote is applied when a hospital did not have any cases meet the inclusion criteria for a measure."
  },
  8: {
    "information": "The lower limit of the confidence interval cannot be calculated if the number of observed infections equals zero. None"
  },
  9: {
    "information": "No data are available from the state/territory for this reporting period. This footnote is applied when: • Too few hospitals in a state/territory had data available or • No data was reported for this state/territory.",
    POOR_SAMPLE_KEY: True,
  },
  10: {
     "information": "Very few patients were eligible for the HCAHPS survey. The scores shown reflect fewer than 50 completed surveys. Use these scores with caution, as the number of surveys may be too low to reliably assess hospital performance. This footnote is applied when the number of completed surveys the hospital or its vendor provided to CMS is less than 50.",
     POOR_SAMPLE_KEY: True,
    },
  11: {
     "information": "There were discrepancies in the data collection process. This footnote is applied when there have been deviations from data collection protocols. CMS is working to correct this situation.",
     POOR_SAMPLE_KEY: True,
    },
  12: {
     "information": "This measure does not apply to this hospital for this reporting period. This footnote is applied when: • There were zero device days or procedures for the entire reporting period, • The hospital does not have ICU locations. • The hospital is a new member of the registry or reporting program and didn’t have an opportunity to submit any cases; or • The hospital doesn't report this voluntary measure; or • Results for this VA hospital are combined with those from the VA administrative parent hospital that manages all points of service.",
     POOR_SAMPLE_KEY: True,
    },
  13: {
     "information": "Results cannot be calculated for this reporting period. This footnote is applied when: • The number of predicted infections is less than 1. • The number of observed MRSA or Clostridium difficile infections present on admission (community-onset prevalence) was above a pre-determined cut-point.",
     POOR_SAMPLE_KEY: True,
    },
  14: {
     "information": "The results for this state are combined with nearby states to protect confidentiality. This footnote is applied when a state has fewer than 10 hospitals in order to protect confidentiality. Results are combined as follows: (1) the District of Columbia and Delaware are combined; (2) Alaska and Washington are combined; (3) North Dakota and South Dakota are combined; and (4) New Hampshire and Vermont are combined. Hospitals located in Maryland and U.S. territories are excluded from the measure calculation."
    },
  15: {
     "information": "The number of cases/patients is too few to report a star rating. This footnote is applied when the number of completed surveys the hospital or its vendor provided to CMS is less than 100. In order to receive HCAHPS Star Ratings, hospitals must have at least 100 completed HCAHPS Surveys over a four-quarter period.",
     POOR_SAMPLE_KEY: True,
    },
  16: {
     "information": "There are too few measures or measure groups reported to calculate a star rating or measure group score. This footnote is applied when a hospital: • Reported data for fewer than 3 measures in any measure group used to calculate star ratings; or • Reported data for fewer than 3 of the measure groups used to calculate star ratings; or  • Did not report data for at least 1 outcomes measure group.",
     POOR_SAMPLE_KEY: True,
    },
  17: {
     "information": "This hospital’s star rating only includes data reported on inpatient services. This footnote is applied when a hospital only reports data for inpatient hospital services.",
     POOR_SAMPLE_KEY: True,
    },
  18: {
     "information": "This result is not based on performance data; the hospital did not submit data and did not submit an HAI exemption form. This footnote is applied when a hospital did not submit data through the National Healthcare Safety Network (NHSN) and did not have a HAI exemption on file. In such a case, the hospital receives the maximum Winsorized z-score.",
     POOR_SAMPLE_KEY: True,
    },
  19: {
     "information": "Data are shown only for hospitals that participate in the Inpatient Quality Reporting (IQR) and Outpatient Quality Reporting (OQR) programs. Footnote is applied for those hospitals that do not participate in the IQR, OQR programs.",
     POOR_SAMPLE_KEY: True,
    },
  20: {
     "information": "State and national averages do not include Veterans Health Administration (VHA) hospital data. Data for VHA hospitals are calculated separately from data for other inpatient acute-care hospitals. This footnote is no longer used."
    },
  21: {
     "information": "Patient survey results for Veterans Health Administration (VHA) hospitals do not represent official HCAHPS results and are not included in state and national averages. The VHA Survey of Healthcare Experiences of Patients (SHEP) inpatient survey uses the same questions as the HCAHPS survey but is collected and analyzed independently. This footnote is no longer used."
    },
  22: {
     "information": "Overall star ratings are not calculated for Veterans Health Administration (VHA) or Department of Defense (DoD) hospitals. • VHA hospitals are not included in the calculations of the Hospital Compare overall rating. • DoD hospitals are not included in the calculations of the Hospital Compare overall rating or the HCAHPS star ratings.",
     POOR_SAMPLE_KEY: True,
    },
  23: {
    "information": "The data are based on claims that the hospital or facility submitted to CMS. The hospital or facility has reported discrepancies in their claims data. ◆ This footnote is applied when a hospital or facility alerts CMS of a possible issue with the claims data used to calculate results for this measure. Calculations are based on a “snapshot” of the administrative claims data and changes that hospitals or facilities make to their claims after the snapshot are not reflected in the data. Issues with claims data include but are not limited to the use of incorrect billing codes or inaccurate dates of service.",
    POOR_SAMPLE_KEY: True,
  },
  24: {
     "information": "Results for this VA hospital are combined with those from the VA administrative parent hospital that manages all points of service. This footnote is applied to VA hospitals only. State and national averages include Veterans"
    },
  25: {
     "information": "Health Administration (VHA) hospital data. State and national averages include Department of"
    },
  26: {
     "information": "Defense (DoD) hospital data."
    },
  27: {
     "information": "* Data for VHA hospitals are calculated along with data for other inpatient acute-care hospitals. Data for DoD hospitals are calculated along with data for other inpatient acute-care hospitals. The DoD TRICARE Inpatient Satisfaction Survey (TRISS) uses the same questions as the HCAHPS survey but is collected and analyzed independently."
    },
}