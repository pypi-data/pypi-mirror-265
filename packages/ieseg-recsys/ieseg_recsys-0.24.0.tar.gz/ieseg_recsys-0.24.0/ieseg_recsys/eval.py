import pandas as pd 
import numpy as np 
from numpy.linalg import norm
from sklearn.metrics import ndcg_score, roc_auc_score, roc_curve
import surprise
from collections.abc import Iterable

def simil_cosine(a,b):
    return np.dot(a, b)/(norm(a)*norm(b))

def pearson_corr(a,b):
    return np.corrcoef(a, b)[0,1]

# compute RMSE
def rmse(pred, real):
    return np.sqrt(((pred - real) ** 2).mean())

# compute MAE
def mae(pred, real):
    return np.absolute(np.subtract(real, pred)).mean()

def ndcg(prediction, real, topn):
    res = []
    for rl, pred in zip(real, prediction):
        # overlap between predictions and real preferences
        common = set(rl).intersection(set(pred))
        # extract ranking of common items
        rl_rank = [rl.index(x) for x in common]
        pred_rank = [pred.index(x) for x in common]

        # compute NDCG
        if len(rl_rank) == 1: 
            if rl_rank==pred_rank: res.append(1.0)
            else: res.append(0.0)
        else:
            res.append(ndcg_score([rl_rank[:topn]], [pred_rank[:topn]]))
    return np.mean(res)

# check if input is pandas DataFrame
def isDataFrame(x):
    return isinstance(x, pd.DataFrame)

# convert predictions from pandas DataFrame to surprise.Prediction
def df2surprise(df):
    return [surprise.Prediction(*i) for i in df.itertuples(index=False)]

# Wrapper for accuracy metrics
def prediction_metrics(prediction, excl_impossible=False):

    if isDataFrame(prediction):
        prediction = df2surprise(prediction)

    pred = []
    real = [] 

    res = {}
    if excl_impossible:
        if all(isinstance(i, surprise.Prediction) for i in pred):

            # filter impossible prediction (np.array([True, False, True, ...])) 
            for i in prediction:
                if not i.details["was_impossible"]:
                    pred.append(i.est)
                    real.append(i.r_ui) 
            print(f'Excluded {len(prediction) - len(pred)} ({len(prediction)}) samples. {len(pred)} remaining ...')
        else:
            raise Exception(f"Argument 'prediction' not of type -> List[surprise.Prediction]")
    else:

        for i in prediction:
            pred.append(i.est)
            real.append(i.r_ui)

    # compute accuracy metrics
    res['RMSE'] = [rmse(np.array(pred), np.array(real))]
    res['MAE'] = [mae(np.array(pred), np.array(real))]
    
    # return pd.DataFrame
    return pd.DataFrame(res, index=['value']).T


def classification_metrics(prediction, threshold, topn=False, excl_impossible=False):

    if isDataFrame(prediction):
        prediction = df2surprise(prediction)

    list_metrics = ['Recall', 'Precision', 'F1']

    if topn:
        print('Warning: TopN classification not recommended to use ...')

        if excl_impossible:
            prediction = [i for i in prediction if not i.details["was_impossible"]]

        df_pred_sort = {}
        df_real_sort = {}
        df_pred = pd.DataFrame(prediction)

        # sort user preferences by rating
        for user in df_pred['uid'].unique():
            # predicted values
            plist = list(df_pred.loc[df_pred['uid']==user,:].sort_values('est', ascending=False)['iid'])
            df_pred_sort[user] = [plist]
            
            # real values
            rlist = list(df_pred.loc[df_pred['uid']==user,:].sort_values('r_ui', ascending=False)['iid'])
            df_real_sort[user] = [rlist]

        df_pred_sort = pd.DataFrame(df_pred_sort, index=['item']).T
        df_real_sort = pd.DataFrame(df_real_sort, index=['item']).T
        
        # check for consistency in recommended items
        if (len(set([len(i[:threshold]) for i in df_pred_sort["item"]])) > 2):
            print('Warning: Missing items in TopN predictions may lead to imprecise metrics ...')

        list_tp = []
        list_fp = []
        list_fn = []

        # compute overlap recommendations and true user preferences
        for pred, real in zip(df_pred_sort["item"], df_real_sort["item"]):
            common = len(np.intersect1d(pred[:threshold], real[:threshold]))
            list_tp.append(common)
            list_fp.append(len(pred[:threshold]) - common)
            list_fn.append(len(real[:threshold]) - common)
        TP = np.sum(list_tp)
        FP = np.sum(list_fp)
        FN = np.sum(list_fn)

        list_metrics = [f'Recall@{threshold}', f'Precision@{threshold}', f'F1@{threshold}']
    
    else:
        pred = []
        real = [] 

        if excl_impossible:
            if all(isinstance(i, surprise.Prediction) for i in pred):

                # filter impossible prediction (np.array([True, False, True, ...])) 
                for i in prediction:
                    if not i.details["was_impossible"]:
                        pred.append(i.est)
                        real.append(i.r_ui) 
                print(f'Excluded {len(prediction) - len(pred)} ({len(prediction)}) samples. {len(pred)} remaining ...')
            else:
                raise Exception(f"Argument 'prediction' not of type -> List[surprise.Prediction]")
                
        else:
            for i in prediction:
                pred.append(i.est)
                real.append(i.r_ui)

        pred = np.array(pred)
        real = np.array(real)
        
        # compute confusion matrix
        TP = np.sum((pred >= threshold) & (real >= threshold))
        FP = np.sum((pred >= threshold) & (real < threshold))
        FN = np.sum((pred < threshold) & (real >= threshold))
        TN = np.sum((pred < threshold) & (real < threshold))


    # compute Recall, Precision, F1
    recall    = TP / (TP+FN)
    precision = TP / (TP+FP)
    f1        = (2*precision*recall) / (precision+recall)

    df = pd.DataFrame([recall, precision, f1], index=list_metrics, columns=['value'])

    return df

def is_iter(x):
    return not isinstance(x, str) and isinstance(x, Iterable)


def ranking_metrics(prediction, threshold, excl_impossible=False):

    if isDataFrame(prediction):
        prediction = df2surprise(prediction)

    if excl_impossible:
        prediction = [i for i in prediction if not i.details["was_impossible"]]

    df_pred_sort = {}
    df_real_sort = {}
    df_pred = pd.DataFrame(prediction)

    # sort user preferences by rating
    for user in df_pred["uid"].unique():
        # predicted values
        plist = list(df_pred.loc[df_pred["uid"]==user,:].sort_values("est", ascending=False)["iid"])
        
        # real values
        rlist = list(df_pred.loc[df_pred["uid"]==user,:].sort_values("r_ui", ascending=False)["iid"])

        # plist and rlist should be longer than 0
        if len(plist) == 0 or len(rlist) == 0: 
            continue
        else:
            df_pred_sort[user] = [plist]
            df_real_sort[user] = [rlist]

    df_pred_sort = pd.DataFrame(df_pred_sort, index=["iid"]).T
    df_real_sort = pd.DataFrame(df_real_sort, index=["iid"]).T

    res = {}

    res[f'NDCG@{threshold}'] = ndcg(df_real_sort["iid"], df_pred_sort["iid"], threshold)

    return pd.DataFrame(res, index=['value']).T

def evaluate(prediction, topn, rating_cutoff, excl_impossible=False):
    if isDataFrame(prediction):
        prediction = df2surprise(prediction)
    return pd.concat([
        prediction_metrics(prediction, excl_impossible=excl_impossible),
        classification_metrics(prediction, rating_cutoff, excl_impossible=excl_impossible),
        ranking_metrics(prediction, topn, excl_impossible=excl_impossible)
        ])

###################################
# Evaluate Top-N recommendations  #
###################################

def ap(prediction, real, topn=10):
    if len(prediction)>topn:
        prediction = prediction[:topn]
    
    score = 0.0
    num_hits = 0.0

    for i,p in enumerate(prediction):
        if p in real and p not in prediction[:i]:
            num_hits += 1.0
            score += num_hits / (i+1.0)

    if not real:
        return 0.0

    return score / min(len(real), topn)

def map(prediction, real, topn=10):
    return np.mean([ap(p,r,topn) for p,r in zip(prediction, real)])

def is_iter(x):
    return not isinstance(x, str) and isinstance(x, Iterable)

def hr(prediction, real, topn=10):
    if len(prediction)>topn:
        prediction = prediction[:topn]

    num_hits = 0.0

    for i,p in enumerate(prediction):
        if p in real and p not in prediction[:i]:
            num_hits += 1.0

    if not real:
        return 0.0

    return num_hits / min(len(real), topn)

# def _ndcg(prediction, real, topn):

#     # overlap between predictions and real preferences
#     common = set(real).intersection(set(prediction))

#     # extract ranking of common items
#     rl_rank = [real.index(x) for x in common]
#     pred_rank = [prediction.index(x) for x in common]

#     if len(common) == 0:
#         return 0.0
#     if len(rl_rank) == 1: 
#         if rl_rank==pred_rank:
#             return 1.0
#         else: 
#             return 0.0

#     else:
#         return ndcg_score([rl_rank], [pred_rank], k=topn)


# def ndcg(prediction, real, topn):
#     assert is_iter(prediction), "y_pred is not iterable"
#     assert is_iter(real), "y_true is not iterable"

#     if is_iter(prediction[0]):
#         assert is_iter(real[0]), f"Input type mismatch:\ny_pred {type(prediction)}({type(prediction[0])}),\ny_true {type(real)}({type(real[0])})"
#         assert len(prediction) == len(real), f"Length mismatch:\ny_pred ({len(prediction)}),\ny_true ({len(real)})"
#         # return [_ndcg(p,r,topn) for p,r in zip(prediction, real)]
#         return np.mean([_ndcg(p,r,topn) for p,r in zip(prediction, real)])
#     else:
#         return _ndcg(prediction, real, topn)