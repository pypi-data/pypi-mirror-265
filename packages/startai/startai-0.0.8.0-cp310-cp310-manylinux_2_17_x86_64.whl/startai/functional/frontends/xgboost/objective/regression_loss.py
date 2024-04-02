import startai


class LogisticRegression:
    @staticmethod
    def pred_transform(x):
        return startai.sigmoid(x)

    @staticmethod
    def first_order_gradient(predt, label):
        return predt - label

    @staticmethod
    def second_order_gradient(predt, label):
        return startai.fmax(predt * (1.0 - predt), 1e-16)

    @staticmethod
    def prob_to_margin(base_score):
        return startai.logit(base_score)
