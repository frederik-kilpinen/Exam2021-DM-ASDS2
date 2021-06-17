# Description

This repository contains all the Python code and LaTeX files used for our project. The code is stored in the directory "Notebooks" and organized in Jupyter notebooks corresponding to the different steps of data collection, data processing and methods. More detailed descriptions of the code is given in each notebook.

1. data_collection: Code used for collecting tweets from Australian MPs.
2. data_processing: Code for preprocessing the data. This includes cleaning, merging with external data containing info about MPs and doing text-preprocessing.
3. topic_models: Code for the hSBM and LDA topic model in section 5.2.1 (ASDS2).
4. keyword_subsetting: Here we run the King et. al. (2017) algorithm to generate keywords and subset bushfire tweets (ASDS2).
5. retweet_network: Code for creating the retweet network within the group of MPs and bushfire subset in section 4 (Digital Methods).
6. semantic_network: Code for creating the party-hashtag and mp-cooccurance networks in the sections 4.1.1 and 4.1.2 (Digital Methods).
7. party_prediction: Implementation of Average Marginal Effect estimation for the multinomial logit model and results for section 5.4 (ASDS2)
