import pandas as pd
import os

'''
@authtor: Davis Spradling

@breif: Our goal with this script is to try and parse through the files in all_mag_query and concatenate all the csv files together from different parallel processes. Very simliar
to what is be done in dataframeParser but due to different features being accessed a different script needed to written.
'''

directory_path = os.path.join(os.path.dirname(__file__), "..", "rerun_trial3_dblp_to_mag")

#put file names in list so we can can loop throgh them
file_names = ['rerun_filter_dblp_to_mag_mag_0_15333333_6_3000','rerun_filter_dblp_to_mag_mag_15333333_30666666_6_3000',
              'rerun_filter_dblp_to_mag_mag_30666666_45999999_6_3000','rerun_filter_dblp_to_mag_mag_45999999_61333332_6_3000',
              'rerun_filter_dblp_to_mag_mag_61333332_76666665_6_3000','rerun_filter_dblp_to_mag_mag_76666665_91999998_6_3000',
              'rerun_filter_dblp_to_mag_mag_91999998_107333331_6_3000','rerun_filter_dblp_to_mag_mag_107333331_122666664_6_3000',
              'rerun_filter_dblp_to_mag_mag_122666664_137999997_6_3000','rerun_filter_dblp_to_mag_mag_137999997_153333330_6_3000',
              'rerun_filter_dblp_to_mag_mag_153333330_168666663_6_3000','rerun_filter_dblp_to_mag_mag_168666663_183999996_6_3000',
              'rerun_filter_dblp_to_mag_mag_183999996_199333329_6_3000','rerun_filter_dblp_to_mag_mag_199333329_214666662_6_3000']

#list to hold dataframes
dataframes_list = []

#loop through files and append them to dataframes list
for file in file_names:
    file_path = os.path.join(directory_path, file + ".csv")
    temp_df = pd.read_csv(file_path)
    added_df = pd.DataFrame(temp_df)
    dataframes_list.append(added_df)

all_df = pd.concat(dataframes_list, axis=0)

file_name = 'total_dblp_to_mag_rerun_trial3.csv'

all_df.to_csv(file_name, sep=',', encoding='utf-8')
    
