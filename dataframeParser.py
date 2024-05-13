import pandas as pd
import os

'''
Our goal with this script is to try and parse through the files in testing_parallel_150000 which contains query time data broken up in 15 parallel processes.
To do this we will break up all of the individual files into a seperate Pandas dataframe and then will find the average in all of the columns that we care about. 
'''
#find the directory where files are located
directory_path = os.path.join(os.path.dirname(__file__), "..", "2ndFullMatchingTrial")

#put file names in list so we can can loop throgh them
file_names = ['testing_parallel_matching_script_DBLP_threshold_70_mag_0_15333333_6_3000','testing_parallel_matching_script_DBLP_threshold_70_mag_15333333_30666666_6_3000',
              'testing_parallel_matching_script_DBLP_threshold_70_mag_30666666_45999999_6_3000','testing_parallel_matching_script_DBLP_threshold_70_mag_45999999_61333332_6_3000',
              'testing_parallel_matching_script_DBLP_threshold_70_mag_61333332_76666665_6_3000','testing_parallel_matching_script_DBLP_threshold_70_mag_76666665_91999998_6_3000',
              'testing_parallel_matching_script_DBLP_threshold_70_mag_91999998_107333331_6_3000','testing_parallel_matching_script_DBLP_threshold_70_mag_107333331_122666664_6_3000',
              'testing_parallel_matching_script_DBLP_threshold_70_mag_122666664_137999997_6_3000','testing_parallel_matching_script_DBLP_threshold_70_mag_137999997_153333330_6_3000',
              'testing_parallel_matching_script_DBLP_threshold_70_mag_153333330_168666663_6_3000','testing_parallel_matching_script_DBLP_threshold_70_mag_168666663_183999996_6_3000',
              'testing_parallel_matching_script_DBLP_threshold_70_mag_183999996_199333329_6_3000','testing_parallel_matching_script_DBLP_threshold_70_mag_199333329_214666662_6_3000']


#list to hold dataframes
dataframes_list = []

#loop through files and append them to dataframes list
for file in file_names:
    file_path = os.path.join(directory_path, file + ".csv")
    temp_df = pd.read_csv(file_path)
    added_df = pd.DataFrame(temp_df)
    dataframes_list.append(added_df)
    
#calculate the totals of phase1 and phase2 and total query time 
total_query_phase1 = 0
total_query_phase2 = 0
total_query_total = 0
total_hashmap_build = 0
counter = 0
for frame in dataframes_list:
    total_query_phase1 += frame['average_query_time_phase1'].sum()
    total_query_phase2 += frame['average_query_time_phase2'].sum()
    total_query_total += frame['average_query_time_phase1'].sum() + frame['average_query_time_phase2'].sum()
    total_hashmap_build += frame['hashmap_build_time'].iloc[1]
    counter += len(frame)


print("Average Hashmap Buildtime: ",(total_hashmap_build/len(dataframes_list)))
print("Phase 1 Average Query Time: ",(total_query_phase1/counter))
print("Phase 2 Average Query Time: ",(total_query_phase2/counter))
print("Total Average Query Time: ",(total_query_total/counter))

