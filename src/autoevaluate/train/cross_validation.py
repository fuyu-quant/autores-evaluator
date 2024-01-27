from sklearn.model_selection import KFold
from ..utils.log_config import setup_logging
from .model_template import model_template

result_logger, _ = setup_logging()

def exec_cross_validation(model, dataset, metrix, params, valuation_index):
    result_logger.info('------cross_validataion------')
    X = dataset.drop(columns=['target']).values
    y = dataset['target'].values

    kf = KFold(n_splits=3, shuffle=True, random_state=0)
    i = 0
    index_list = []
    for train_index, test_index in kf.split(X):
        i += 1
        result_logger.info(f'------Round{i}------')
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        y_pred = model_template(model, X_train, y_train, X_test, params)
        index = metrix(y_test, y_pred, valuation_index)
        index_list.append(index)

    average_index = sum(index_list) / len(index_list)
    return average_index
