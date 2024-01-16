from Levenshtein import distance,ratio



#Operations for Levenshtein that add to distance to make strings "equal"
#Insertion: Adding a character to string A.
#Deletion: Removing a character from string A.
#Replacement: Replacing a character in string A with another character


dis = distance("levenshtein", "levenshtein")
print(dis)


#if values are the same we get a 1.0 ration (perfect)
rat = ratio("enshtein", "levenshtein")
print(rat)




