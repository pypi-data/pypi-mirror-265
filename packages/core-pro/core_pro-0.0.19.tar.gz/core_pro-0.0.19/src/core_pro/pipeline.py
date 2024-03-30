import polars as pl
import numpy as np


class ExtractTime:
    @staticmethod
    def month_day(df: pl.DataFrame, col: str = 'grass_date') -> pl.DataFrame:
        return df.with_columns(
            pl.col(col).dt.year().alias('year').cast(pl.Int16),
            pl.col(col).dt.month().alias('month').cast(pl.Int8),
            pl.col(col).dt.day().alias('day').cast(pl.Int8),
        )

    @staticmethod
    def cycle_time(df: pl.DataFrame) -> pl.DataFrame:
        return df.with_columns(
            pl.col('month').map(lambda x: np.sin(2 * np.pi * x / 12)).alias('month_sin'),
            pl.col('month').map(lambda x: np.cos(2 * np.pi * x / 12)).alias('month_cos'),
            pl.col('day').map(lambda x: np.sin(2 * np.pi * x / 31)).alias('day_sin'),
            pl.col('day').map(lambda x: np.cos(2 * np.pi * x / 31)).alias('day_cos'),
            (pl.col('month') - pl.col('day')).alias('days_dif_spike'),
        )

    @staticmethod
    def trend(df: pl.DataFrame, col: list, window: int = 7) -> pl.DataFrame:
        return df.with_columns(
            pl.col(i).rolling_mean(window).alias(f'trend_{window}d_{i}') for i in col
        )

    @staticmethod
    def season(df: pl.DataFrame, col: list, window: int = 7) -> pl.DataFrame:
        return df.with_columns(
            (pl.col(i) - pl.col(f'trend_{window}d_{i}')).alias(f'season_{window}d_{i}') for i in col
        )

    @staticmethod
    def lag(df: pl.DataFrame, col: list, window: int = 7) -> pl.DataFrame:
        return df.with_columns(
            pl.col(i).shift(window).alias(f'shift_{window}d_{i}') for i in col
        )


class LGBMPipeline:
    def __init__(
            self,
            x_train: np.ndarray,
            y_train: np.ndarray,
            x_test: np.ndarray,
            y_test: np.ndarray,
    ):
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test

    def run(
            self,
            report: bool = True,
            params: dict = None,
    ):
        from lightgbm import LGBMClassifier, log_evaluation, early_stopping
        from sklearn.metrics import classification_report

        # params
        if not params:
            params = {
                'metric': 'auc',
                'random_state': 42,
            }

        # train
        self.model = LGBMClassifier(**params)
        self.model.fit(
            self.x_train, self.y_train,
            eval_set=[(self.x_test, self.y_test)],
            callbacks=[log_evaluation(0), early_stopping(50)]
        )

        # predict
        pred = self.model.predict(self.x_test, num_iteration=self.model.best_iteration_)

        # report
        if report:
            print(classification_report(self.y_test, pred))
        return self.model

    def feature_importance(self, all_features: list) -> pl.DataFrame:
        zip_ = zip(all_features, self.model.feature_importances_)
        return (
            pl.DataFrame(zip_, schema=['feature', '# times the feature is used'])
            .sort('# times the feature is used', descending=True)
        )
