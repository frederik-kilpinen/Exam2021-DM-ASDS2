# coding: utf-8

### The following consists code to replicate the results in King, Lam, Roberts. 
### All code was run in Python 3+.


## Load keyword code
from keyword_algorithm import *


#############################

## Keywords from Table 3

boston = Keywords()
boston.ReferenceSet(data='bostonref.csv', text_colname='Contents', id_colname='GUID')
boston.SearchSet(data='bostonsearch.csv', text_colname='Contents', id_colname='GUID')
boston.ProcessData(remove_wordlist=['boston', '#boston', 'bostonbombings', '#bostonbombings'], keep_twitter_symbols=False)

boston.ReferenceKeywords()
boston.ClassifyDocs(algorithms=['nbayes', 'logit'])
boston.FindTargetSet()
boston.FindKeywords()
boston.PrintKeywords()


#############################


# Algorithm Output for Figure 3

# Human experiment data

exp = pd.read_csv('boston_experiment.csv')
words = []
for i in range(len(exp)):
    words = words + [w.strip() for w in exp.iloc[i] if str(w) != 'nan' and len(str(w)) > 0]

words = ProcessText(set(words), keep_twitter_symbols=False).text
words = [w for w in words if len(w) > 0]
exp_df = DataFrame(words, columns=['words'])
exp_df.drop_duplicates(subset='words', inplace=True)
nkeywords = len(exp_df)

t = list(boston.search_set.id[boston.search_set.Target == 1])
len(t)


boston.ViewDocs(any_words=boston.target_keywords[0:len(exp_df)], nprint=0, doc_set='search')
found = boston.viewed_docs
r = len(set(found).intersection(set(t)))/len(t)
p = len(set(found).intersection(set(t)))/len(found)
print(r,p)


boston.ViewDocs(any_words=list(exp_df.words), nprint=0, doc_set='search')
found = boston.viewed_docs
r = len(set(found).intersection(set(t)))/len(t)
p = len(set(found).intersection(set(t)))/len(found)
print(r,p)

t_cum_recall = []
t_cum_precision = []
nt_cum_recall = []
nt_cum_precision = []
for i in range(1, 101):
    boston.ViewDocs(any_words = boston.target_keywords[0:i], doc_set='search', nprint=0)
    found = boston.viewed_docs
    t_cum_recall.append(len(set(found).intersection(set(t)))/len(t))
    t_cum_precision.append(len(set(found).intersection(set(t)))/len(found))
    boston.ViewDocs(any_words = boston.nontarget_keywords[0:i], doc_set='search', nprint=0)
    found = boston.viewed_docs
    nt_cum_recall.append(len(set(found).intersection(set(t)))/len(t))
    nt_cum_precision.append(len(set(found).intersection(set(t)))/len(found))



cum_recall = DataFrame(t_cum_recall + nt_cum_recall, columns=['Recall'])
cum_recall['Set'] = ['Target'] * 100 + ['Non-Target'] * 100
cum_recall['Word'] = list(range(1, 101)) * 2
cum_precision = DataFrame(t_cum_precision + nt_cum_precision, columns=['Precision'])
cum_precision['Set'] = ['Target'] * 100 + ['Non-Target'] * 100
cum_precision['Word'] = list(range(1, 101)) * 2

cum_recall.to_csv('cum_recall.csv', index=False)
cum_precision.to_csv('cum_precision.csv', index=False)


#############################


# Algorithm Output for Figure 4 Overall Precision/Recall

# Calculate precision and recall for human keywords

exp_recall = []
exp_precision = []
for w in exp_df.words:
    boston.ViewDocs(any_words = w, doc_set='search', nprint=0)
    found = boston.viewed_docs
    exp_recall.append(len(set(found).intersection(set(t)))/len(t))
    if len(found) == 0:
        exp_precision.append('')
    else:
        exp_precision.append(len(set(found).intersection(set(t)))/len(found))

exp_df['recall'] = exp_recall
exp_df['precision'] = exp_precision
exp_df.sort(columns=['precision', 'recall'], inplace=True, ascending=False)

# Calculate precision and recall for algorithm keywords

t_recall = []
t_precision = []
#nt_recall = []
#nt_precision = []
#for i in range(1, len(exp_df)):
#    boston.ViewDocs(any_words = boston.target_keywords[0:i], doc_set='search', nprint=0)
for w in boston.target_keywords[0:nkeywords]:
    boston.ViewDocs(any_words = w, doc_set='search', nprint=0)
    found = boston.viewed_docs
    t_recall.append(len(set(found).intersection(set(t)))/len(t))
    t_precision.append(len(set(found).intersection(set(t)))/len(found))
    #boston.ViewDocs(none_words = boston.nontarget_keywords[0:i], doc_set='search', nprint=0)
    #found = boston.viewed_docs
    #nt_recall.append(len(set(found).intersection(set(t)))/len(t))
    #nt_precision.append(len(set(found).intersection(set(t)))/len(found))


recall = DataFrame(t_recall, columns=['Algorithm'])
recall['Humans'] = list(pd.to_numeric(exp_df.recall))
precision = DataFrame(t_precision, columns=['Algorithm'])
precision['Humans'] = list(pd.to_numeric(exp_df.precision))
recall = pd.melt(recall)
precision = pd.melt(precision)
recall.columns = ['Method', 'Recall']
precision.columns = ['Method', 'Precision']

precision.to_csv('precision.csv', index=False)
recall.to_csv('recall.csv', index=False)


#############################


# Algorithm output for Figure 4 individual Precision/Recall

boston = Keywords()
boston.ReferenceSet(data='bostonref.csv', text_colname='Contents', id_colname='GUID')
boston.SearchSet(data='bostonsearch.csv', text_colname='Contents', id_colname='GUID')
boston.ProcessData(remove_wordlist=['boston', '#boston', 'bostonbombings', '#bostonbombings'], keep_twitter_symbols=False)
boston.ReferenceKeywords()
boston.ClassifyDocs(algorithms=['nbayes', 'logit'])
boston.FindTargetSet()
boston.FindKeywords()


t = list(boston.search_set.id[boston.search_set.Target == 1])
len(t)

rcomp = pd.DataFrame()
pcomp = pd.DataFrame()
for i in range(len(exp)):
    human = [x for x in list(exp.iloc[i]) if str(x) != 'nan']
    tmp_r = []
    tmp_p = []
    for w in range(1, len(human)+1):
        boston.ViewDocs(any_words=human[0:w], doc_set='search', nprint=0)
        found = boston.viewed_docs
        tmp_r.append(len(set(found).intersection(set(t)))/len(t))
        if len(set(found)) == 0:
            tmp_p.append('NA')
        else:
            tmp_p.append(len(set(found).intersection(set(t)))/len(found))
    tmp_r = tmp_r + ['NA']*(50-len(human))
    tmp_p = tmp_p + ['NA']*(50-len(human))
    rcomp['human'+str(i)] = tmp_r
    pcomp['human'+str(i)] = tmp_p
    
tmp_r = []
tmp_p = []
for w in range(1, 51):
    boston.ViewDocs(any_words=boston.target_keywords[0:w], doc_set='search', nprint=0)
    found = boston.viewed_docs
    tmp_r.append(len(set(found).intersection(set(t)))/len(t))
    if len(set(found)) == 0:
        tmp_p.append('NA')
    else:
        tmp_p.append(len(set(found).intersection(set(t)))/len(found))
rcomp['algorithm'] = tmp_r
pcomp['algorithm'] = tmp_p


rcomp.to_csv('recall_allhuman.csv', index=False)
pcomp.to_csv('precision_allhuman.csv', index=False)


#############################


# Algorithm Output for Figure 5

cum_recall_sizes = DataFrame()
cum_precision_sizes = DataFrame()


for size in [108,500,1000,2500,4000]:
    ss = 'bostonsearch' + str(size) + '.csv'
    boston = Keywords()
    boston.ReferenceSet(data='bostonref.csv', text_colname='Contents', id_colname='GUID')
    boston.SearchSet(data=ss, text_colname='Contents', id_colname='GUID')
    boston.ProcessData(remove_wordlist=['boston', '#boston', 'bostonbombings', '#bostonbombings'], keep_twitter_symbols=False)
    boston.ReferenceKeywords()
    boston.ClassifyDocs(algorithms=['nbayes', 'logit'])
    boston.FindTargetSet()
    boston.FindKeywords()
    t = list(boston.search_set.id[boston.search_set.Target == 1])
    print(len(t))
    t_cum_recall = []
    t_cum_precision = []
    nt_cum_recall = []
    nt_cum_precision = []
    t_recall = []
    t_precision = []
    nt_recall = []
    nt_precision = []
    for w in boston.target_keywords[0:100]:
        boston.ViewDocs(any_words = w, doc_set='search', nprint=0)
        found = boston.viewed_docs
        t_recall.append(len(set(found).intersection(set(t)))/len(t))
        t_precision.append(len(set(found).intersection(set(t)))/len(found))
    for w in boston.nontarget_keywords[0:100]:
        boston.ViewDocs(any_words = w, doc_set='search', nprint=0)
        found = boston.viewed_docs
        nt_recall.append(len(set(found).intersection(set(t)))/len(t))
        nt_precision.append(len(set(found).intersection(set(t)))/len(found))
    for i in range(1, 101):
        boston.ViewDocs(any_words = boston.target_keywords[0:i], doc_set='search', nprint=0)
        found = boston.viewed_docs
        t_cum_recall.append(len(set(found).intersection(set(t)))/len(t))
        t_cum_precision.append(len(set(found).intersection(set(t)))/len(found))
        boston.ViewDocs(any_words = boston.nontarget_keywords[0:i], doc_set='search', nprint=0)
        found = boston.viewed_docs
        nt_cum_recall.append(len(set(found).intersection(set(t)))/len(t))
        nt_cum_precision.append(len(set(found).intersection(set(t)))/len(found))

    cum_recall_tmp = DataFrame(t_cum_recall + nt_cum_recall, columns=['Recall'])
    cum_recall_tmp['Set'] = ['Target'] * 100 + ['Non-Target'] * 100
    cum_recall_tmp['Word'] = list(range(1, 101)) * 2
    cum_recall_tmp['Size'] = round(size/100)
    cum_precision_tmp = DataFrame(t_cum_precision + nt_cum_precision, columns=['Precision'])
    cum_precision_tmp['Set'] = ['Target'] * 100 + ['Non-Target'] * 100
    cum_precision_tmp['Word'] = list(range(1, 101)) * 2
    cum_precision_tmp['Size'] = round(size/100)
    cum_recall_sizes = cum_recall_sizes.append(cum_recall_tmp)
    cum_precision_sizes = cum_precision_sizes.append(cum_precision_tmp)

cum_recall_sizes.to_csv('cum_recall_sizes.csv', index=False)
cum_precision_sizes.to_csv('cum_precision_sizes.csv', index=False)


#############################

## Appendix partial demo of workflow

paris = Keywords()
paris.ReferenceSet(data='parisref.csv', text_colname='Contents', id_colname='GUID')
paris.SearchSet(data='parissearch.csv', text_colname='Contents', id_colname='GUID')
paris.ProcessData(remove_wordlist=['paris', '#paris', 'parisattacks', '#parisattacks'], keep_twitter_symbols=False)

paris.ReferenceKeywords()
paris.ClassifyDocs(algorithms=['nbayes', 'logit'])
paris.FindTargetSet()
paris.FindKeywords()
paris.PrintKeywords()

