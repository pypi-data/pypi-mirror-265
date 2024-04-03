<!-- DOCUMENT STYLE -->
<!-- <style>
    body {
        font-family: "Calibri";
        padding-left:1.5cm;
        padding-right:1.5cm;
    }
</style> -->

<!-- HEADER -->
|  |  |
|---|---|
| <img src="https://www.ieseg.fr/wp-content/uploads/IESEG-Logo-2012-rgb.jpg" alt="drawing" width=100%/> | <span><br>Recommendation Systems<br>Module<br>Class: 2023 & 2024</span> |

<!-- CONTENT -->

---

## Overview

- Model evaluation (`eval.py`):
    - Regression metrics
        - RMSE
        - MAE
    - Classification metrics
        - Precision
        - Recall
        - F1
    - Ranking metrics
        - NDCG
    - `eval.evaluate` computes all above mentioned metrics 
    - Evaluate Top-N recommendations
        - HR
        - MAP
- Content based Recommender System (`model.py`)
- Helper functions (`utils.py`)
    - `get_top_n`: Compute Top-N recommendations from predictions 
    - `predict_user_topn`: Compute Top-N recommendations for a user 

<br>

| Useful Links |  |
|---|---|
 | <a href="https://surpriselib.com/"><img src="https://surpriselib.com/logo_white.svg" width="100%"></a> | <a href="https://scikit-learn.org/stable/"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Scikit_learn_logo_small.svg/2560px-Scikit_learn_logo_small.svg.png" width="25%"></a> |