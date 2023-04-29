Yuehan Qin yqin18@stevens.edu, 
# the URL of your public GitHub repo
https://github.com/JJthomps-prog/project3.git.  
# an estimate of how many hours you spent on the project
40 hours
# a description of how to tested the code
Overall: run test.sh.  
For Baseline: we test our codes with forum_multiple_posts.postman_collection.json,forum_post_read_delete.postman_collection.json.  
For Date- and time-based range queries: we test our codes with search.json.   
# any bugs or issues could not resolve

# an example of a difficult issue or bug and how you resolved
We need to convert datetime to ISO 8601 format at first.   
# a list of the four extensions you’ve chosen to implement
Date- and time-based range queries.  
# detailed summaries of your tests for each of your extensions
Date- and time-based range queries:To tell wheather it is valid start time and end time, if the start time is after the end time it raise an error, if the user didn't provide the time, it raise an error.  
