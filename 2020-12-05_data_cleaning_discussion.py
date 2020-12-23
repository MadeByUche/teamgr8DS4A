############################################################
# # hospital_general_information
############################################################
# data_file_name = "Hospital_General_Information.csv"

# # TODO(anewla): columns, lower case and underscore
# # Comma delimmited

# # TODO(anewla): cleaning process
# ##It looks like zeroes need to be added and the zip codes converted to string to maintain the integrity.

# gc['ZIP Code'] = gc['ZIP Code'].astype(str).str.zfill(5).sort_values(ascending=False)
# gc.groupby(['ZIP Code']).size().sort_values(ascending=False)

# # TODO(anewla): ***Adding Full address
# gc['Full Address'] = gc['Address'] + ' ' + gc['City'] + ', ' + gc['State'] + ' ' + gc['ZIP Code']

# # Replacing 'Not Available' values in hopsital overall ratings
# gc['Hospital overall rating'].replace('Not Available', np.nan, inplace = True)

# # TODO(anewla): Convert Location which is of style POINT (-121.77291599999998 37.246742)
# # To lat and lng col
# # TODO(anewla): Geocode using Full Address


# # TODO(anewla): drop footnote columns

# # TODO(anewla): categorization of .* national comparison
# # {
# #  'Above the national average': 2
# # 'Same as the national average': 1
# # 'Below the national average': 0
# # 'Not Available': np.nan
# # }

# # TODO(anewla): typing of values

# # Write new dataset
# # gc_new.to_csv('Hospital_General_Information_Cleaned.csv')
# # !cp Hospital_General_Information_Cleaned.csv "drive/My Drive/"

# # ANALYSIS - Interesting GroupBy's
# # State, City
# # Hospital Ownership, Hospital Type
############################################################



############################################################
# # homeland_infrastructure_foundation_level_data_hfild
############################################################
# data_file_name = "Hospitals.csv"

# # ZIP Fill
# hsptl['ZIP'] = hsptl['ZIP'].astype(str).str.zfill(5).sort_values(ascending=False)
# hsptl.groupby(['ZIP']).size().sort_values(ascending=False)

# # TODO Create Full Address
# hsptl['Full Address'] = hsptl['ADDRESS'] + ' ' + hsptl['CITY'] + ', ' + hsptl['STATE'] + ' ' + hsptl['ZIP']
# hsptl

# # TODO see notion page for all valuable columns

# # TODO(anewla): cleaning up 'NOT AVAILABLE' and replacing with NaN's

# # TODO(anewla): typing of values

# # ANALYSIS - Interesting GroupBy's
# # State, City
# # ZIP
############################################################




############################################################
# # Timely and effective care hospital
############################################################
# data_file_name = 'Timely_and_Effective_Care_-_Hospital.csv'

# # TODO(anewla): zip code fill
# tec['ZIP Code'] = tec['ZIP Code'].astype(str).str.zfill(5).sort_values(ascending=False)
# tec.groupby(['ZIP Code']).size().sort_values(ascending=False)

# # TODO(anewla): full address
# tec['Full Address'] = tec['Address'] + ' ' + tec['City'] + ', ' + tec['State'] + ' ' + tec['ZIP Code']
# tec

# # TODO(anewla): nan filling for Sample, Footnote

# # TODO(anewla): further investigation footnote column
############################################################




############################################################
# # person and community engagement
############################################################
# data_file_name = "Hospital_Value-Based_Purchasing__HVBP____Patient_Experience_of_Care_Domain_Scores__HCAHPS_.csv"

# # TODO(anewla): replacement of 'Not Available' with nan

# # TODO(anewla): columns with values ranging from 0 to 10 need to be sliced (instead of 'x out of 10', replace with 'x')
# # columns with ".* Points"
# lst = [12, 13, 14, 20, 21, 22, 28, 29, 30, 36, 37, 38, 44, 45, 46, 52, 53, 54, 60, 61, 62, 68, 69, 70]
# columns = list(df.iloc[:,lst].columns)
# for i in columns:
#   df[i] = df[i].str.slice(0, 1)


# #**** TODO(anewla): Cleanning up location
# # clean Location column (remove characters, split into lat and long columns, and change to type float)
# df['Location'] = df['Location'].str.slice(start=7, stop=-1)
# df[['Latitude', 'Longitude']] = df['Location'].str.split(expand=True)
# df.drop(columns='Location', inplace=True)

# # TODO(anewla): typing
# # change data type of measure columns to be of type float
# columns = list(df.iloc[:,7:75].columns)
# for i in columns:
#   df[i] = pd.to_numeric(df[i], errors='coerce')
############################################################





############################################################
# # hospital value based performance
############################################################
# data_file_name = "hvpb.csv"


# # TODO(anewla): full address
# patient_exp['Full Address'] = patient_exp.apply(lambda x: x['Address'] + ','+ x['City'] + ',' + x['State'] , axis = 1)


# # TODO(anewla): GEOCODING

# patient_exp['Coordinates'] = ""
# #Generate Coordinates using the Full Adress
# #Didn't want to replace 'Location' with 'Coordinates' until we discuss it
# #Location column is POINT(longitude, latitude) and the longitude and latitude match the ones in coordinates
# geolocator = Nominatim(user_agent="Address Predictor", timeout=5) 
# def custom_geocode(row):
#     lat_long = geolocator.geocode(row['Full Address'])
#     if lat_long:
#       location = ','.join([str(lat_long.latitude), str(lat_long.longitude)])
#     else:
#       location = 'None,None'
#     print(location)
#     return location

# patient_exp['Coordinates'] = patient_exp.apply(lambda x: custom_geocode(x), axis=1)

# # TODO(anewla): 'Not Avaialble' replacement
# # check for columns with 'Not Available' string values and replace with NaN values
# columns = list(patient_exp.iloc[:,7:15].columns)
# for i in columns:
#   patient_exp[i] = patient_exp[i].replace('Not Available', np.NaN)

# # TODO(anewla): cleaning columns for specific - facility id's for parens `330201`
# patient_exp.loc[patient_exp['facility_id'] == 330201, 'unweighted_normalized_clinical_outcomes_domain_score'] = '63.333333333333'
# patient_exp.loc[patient_exp['facility_id'] == 330201, 'weighted_normalized_clinical_outcomes_domain_score'] = '15.833333333333'
# patient_exp.loc[patient_exp['facility_id'] == 330201, 'total_performance_score'] = '24.083333333333'


# # TODO(anewla): data typing
# # total_performance_score: float64
# # change data type of domain columns to be of type float
# columns = list(patient_exp.iloc[:,7:15].columns)
# for i in columns:
#   patient_exp[i] = pd.to_numeric(patient_exp[i], errors='coerce')
############################################################




############################################################
# # complications and deaths
############################################################

# data_file_name = 'complications&deaths.csv'

# # TODO(anewla): columns we don't care about
# # Remove Footnote, Start Date and End Date columns, no need for them
# complications_deaths.drop(['Footnote', 'Start Date', 'End Date'], axis=1, inplace=True)

# # TODO(anewla): replace Not Available and Not Applicable with nan
# complications_deaths = complications_deaths.replace(['Not Available','Not Applicable'], np.nan)

# # TODO(anewla): zip code filling
# # Correct Zip Code values
# complications_deaths['ZIP Code'] = complications_deaths['ZIP Code'].astype(str).str.zfill(5).sort_values(ascending=False)

# # TODO(anewla): categorization for Compared To National column
# cleaned_complications_deaths['Compared to National'] = cleaned_complications_deaths['Compared to National'].astype('category')
# cleaned_complications_deaths['Compared to National'].cat.categories
# #[-1:'Number of Cases Too Small' 0:'Worse Than the National Rate', 1: 'No Different Than the National Rate', 2: 'Better Than the National Rate']
# cleaned_complications_deaths['Compared to National'] = cleaned_complications_deaths['Compared to National'].replace('Number of Cases Too Small', -1)
# cleaned_complications_deaths['Compared to National'] = cleaned_complications_deaths['Compared to National'].replace('Worse Than the National Rate', 0)
# cleaned_complications_deaths['Compared to National'] = cleaned_complications_deaths['Compared to National'].replace('No Different Than the National Rate', 1)
# cleaned_complications_deaths['Compared to National'] = cleaned_complications_deaths['Compared to National'].replace('Better Than the National Rate', 2)


# # TODO(anewla): discussion, what is the most valuable data. do we gain any benefit from creating columns 
# # measure_id_score measure_id_
# # TODO(anewla): are measure id' consistent for each facility? ^^ this required for the above to happen
############################################################