# Large Scale Entity for theAdvisor 📘

## About ℹ️
#### theAdvisor is a project started back in 2013 to help users build a strong bibliography by extending the document set obtained after a first-level search. While there exist ways of looking up papers bibliographies, many of them are inaccurate due to how data is gathered using methods such as computer vision, which has flaws with different formatted papers. 

#### Therefore, we have sourced our data from MAG, DBLP, and Citeseer in a diverse set of file formats such as XML, CSV, and SQL. These datasets cross-reference each other to help us gain strong metadata. However, these datasets cannot be matched directly due to there being slight differences in paper titles such as weird spacing, misspellings, capitalization issues, etc. Which is why the two-phase method we used was implemented. 📚🔍

## Phase 1 🔄
#### To start off, take one set of data that you would want to match and break it up into a certain number k-mer. The k value in k-mer varies depending on the size of the entities you want to match but anywhere from 4-8 is recommended. Next, take the k-mer value and its associated unique key (probably some kind of ID) and add it to the hashmap. Then take the other set of data that needs to be matched and parse through it so that for every single title that must be matched, it is broken up into k-mer and found in the hashmap that was just made. Extract all of the unique IDs for each k-mer that the title is broken up into and find the most frequent ID. This will be your match. **Reference the image below that shows how k-mer hashing works** 📝

## Phase 2 🔄
#### While Phase 1 is very efficient, it does have flaws when matching. Especially when having to match high volume data, as often some information loss techniques must be used to give us a feasible runtime to make the project possible. For example, when originally evaluating the runtimes of the k-mer process running at 3-mer alone took about 12.72 seconds per query given a choice of 1,000,000 entities. When removing the top 1000 most frequent 3-mers this reduced the runtime to .69 seconds per query given a choice of 1,000,000 entities. Therefore, given that we were working with such high volume (given that MAG has 210,000,000 entities) it made sense to deal with some information loss to give us a realistic runtime. However, if we can get the correct entity in the top 10 of the k-mer hashing process, we could then use a more expensive and highly accurate algorithm to help make sure that we can confirm we are matching the same entity. The algorithm used in this process is Levenshtein Distance, which is a measure of how different two entities are using three different operations. These being swap, delete, and insert. The exact method used in this project was to move the top 10 matches from k-mer hashing onto the Levenshtein distance process. During this, it would compare the ratio of the candidate entity and the entity that was "matched." If a ratio of .90 or higher was achieved between the two, it qualified as a correct match. **Reference the image below that shows how Levenshtein distance is produced** 📊

## Future Work 🔜
#### With the overall goal of this project being to revivie theAdvisor, a lot of the data sourcing has been completed. However, there are still some web development tasks that need to be completed in order for this project to be launched.

## Contact ✉️
#### For any questions or inquiry about this project please reach out to dspradl1@uncc.edu!
