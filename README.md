Yuehan Qin yqin18@stevens.edu,Zhengyuan Han zhan24@stevens.edu 
# the URL of your public GitHub repo
https://github.com/JJthomps-prog/project3.git.  
# an estimate of how many hours you spent on the project
40 hours
# a description of how to tested the code
Overall: run test.sh.  
For Baseline: we test our codes with forum_multiple_posts.postman_collection.json,forum_post_read_delete.postman_collection.json.  
For Date- and time-based range queries: we test our codes with search.json.   
For "Users and user keys" and "User profiles": we test our codes with user.postman_collection.json and user_info.postman_environment.json.  
For "User-based range queries": we test our codes with User-based_range_queries.postman_collection.json and user_info.postman_environment.json.  
For "Fulltext search": we test our codes with fulltext_search.postman_collection.json and user_info.postman_environment.json.  
# any bugs or issues could not resolve

# an example of a difficult issue or bug and how you resolved
We need to convert datetime to ISO 8601 format at first.   
# a list of the four extensions you’ve chosen to implement
Date- and time-based range queries.  
Users and user keys.  
User profiles.  
User-based range queries.  
Fulltext search.  
# detailed summaries of your tests for each of your extensions
Date- and time-based range queries:To tell wheather it is valid start time and end time, if the start time is after the end time it raise an error, if the user didn't provide the time, it raise an error.  

"Users and user keys" and "User profiles":  
1. Create two users and return their id, keys, usernames, and realnames, we expect the result codes are 200.
2. Create a user with null username and another user with a repeat username, we expect the result codes are 400.
3. Read users' info by id and name, we expect the result codes are 200 and returning correct user info.
4. Edit user info by user key, we expect the result code is 200.
5. Read the user's info again after editting, we expect the result code is 200 and returning correct user info.

"User-based range queries":
1. Create a user and use this user post two messages with the user's info, we expect the result codes are 200.
2. Read messages by author's username and return a list of message info, including msg, time, and author, we expect the result code is 200 and the return list is correct.

"Fulltext search":
1. Create two users and use them post three messges.
2. Search message by text, if a message include the text, return it.
3. We expect the result code is 200 and the return list is correct.
