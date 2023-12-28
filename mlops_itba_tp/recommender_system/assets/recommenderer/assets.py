""" """
import os
from typing import Dict, Tuple

import numpy as np
import pandas as pd
from keras.optimizers import Adam
from tensorflow.keras import Model
from matplotlib import pyplot as plt
from dagster_mlflow import mlflow_tracking
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from dagster import Int, Float, AssetIn, AssetOut, asset, multi_asset

from mlops_itba_tp.recommender_system.assets.recommenderer.model_helper import get_model

mlflow = mlflow_tracking.configured(
    {
        "experiment_name": "recommender-system-II",
        "mlflow_tracking_uri": os.environ.get(
            "MLFLOW_TRACKING_URI", "http://127.0.0.1:8887"
        ),
    }
)


@multi_asset(
    ins={"upstream": AssetIn("training_data")},
    outs={
        "preprocessed_training_data": AssetOut(),
        "user_to_idx": AssetOut(),
        "movie_to_idx": AssetOut(),
    },
)
def preprocess_data(context, upstream: pd.DataFrame) -> Tuple[pd.DataFrame, Dict, Dict]:
    """ """

    context.log.info("Running 'preprocess_data'")

    training_data = upstream

    u_unique = training_data.user_id.unique()
    user_to_idx: Dict = {o: i + 1 for i, o in enumerate(u_unique)}

    m_unique = training_data.movie_id.unique()
    movie_to_idx: Dict = {o: i + 1 for i, o in enumerate(m_unique)}

    training_data["encoded_user_id"] = training_data.user_id.apply(
        lambda x: user_to_idx[x]
    )
    training_data["encoded_movie_id"] = training_data.movie_id.apply(
        lambda x: movie_to_idx[x]
    )

    preprocessed_training_data: pd.DataFrame = training_data.copy()

    return preprocessed_training_data, user_to_idx, movie_to_idx


@multi_asset(
    ins={"preprocessed_training_data": AssetIn()},
    outs={
        "x_train": AssetOut(),
        "x_test": AssetOut(),
        "y_train": AssetOut(),
        "y_test": AssetOut(),
    },
)
def split_data(
    context, preprocessed_training_data: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """ """
    context.log.info("Running 'split_data'")
    test_size = 0.10
    random_state = 42
    x_train, x_test, y_train, y_test = train_test_split(
        preprocessed_training_data[["encoded_user_id", "encoded_movie_id"]],
        preprocessed_training_data[["rating"]],
        test_size=test_size,
        random_state=random_state,
    )
    return x_train, x_test, y_train, y_test


@asset(
    resource_defs={"mlflow": mlflow},
    ins={
        "x_train": AssetIn(),
        "y_train": AssetIn(),
        "user_to_idx": AssetIn(),
        "movie_to_idx": AssetIn(),
    },
    config_schema={
        "batch_size": Int,
        "epochs": Int,
        "learning_rate": Float,
        "embeddings_dim": Int,
    },
)
def keras_dot_product_model(
    context, x_train, y_train, user_to_idx, movie_to_idx
) -> Model:
    """ """

    _mlflow = context.resources.mlflow

    _mlflow.log_params(context.op_config)

    # Model hyperparameters
    batch_size = context.op_config["batch_size"]
    epochs = context.op_config["epochs"]
    learning_rate = context.op_config["learning_rate"]
    embeddings_dim = context.op_config["embeddings_dim"]

    # Model
    model = get_model(len(movie_to_idx), len(user_to_idx), embeddings_dim)
    model.compile(Adam(learning_rate=learning_rate), "mean_squared_error")

    # Model training
    context.log.info(f"batch_size: {batch_size} - epochs: {epochs}")
    history = model.fit(
        [x_train.encoded_user_id, x_train.encoded_movie_id],
        y_train.rating,
        batch_size=batch_size,
        # validation_data=([ratings_val.userId, ratings_val.movieId], ratings_val.rating),
        epochs=epochs,
        verbose=1,
    )

    # Log mlflow data
    for i, l in enumerate(history.history["loss"]):
        _mlflow.log_metric("mse", l, i)

    fig, axs = plt.subplots(1)
    axs.plot(history.history["loss"], label="mse")
    plt.legend()
    _mlflow.log_figure(fig, "plots/loss.png")

    return model


@asset(
    resource_defs={"mlflow": mlflow},
    ins={
        "keras_dot_product_model": AssetIn(),
    },
    name="model_data",
)
def log_model(context, keras_dot_product_model: Model) -> Dict:  # pylint: disable=redefined-outer-name
    """ """
    _mlflow = context.resources.mlflow

    logged_model = _mlflow.tensorflow.log_model(
        keras_dot_product_model,
        "keras_dot_product_model",
        registered_model_name="keras_dot_product_model",
        input_example=[np.array([1, 2]), np.array([2, 3])],
    )

    model_data = {"model_uri": logged_model.model_uri, "run_id": logged_model.run_id}

    return model_data


@asset(
    resource_defs={"mlflow": mlflow},
    ins={
        "model_data": AssetIn(),
        "x_test": AssetIn(),
        "y_test": AssetIn(),
    },
)
def evaluate_model(context, model_data, x_test, y_test) -> None:
    """ """

    _mlflow = context.resources.mlflow

    logged_model = model_data["model_uri"]

    loaded_model = _mlflow.pyfunc.load_model(logged_model)

    y_pred = loaded_model.predict([x_test.encoded_user_id, x_test.encoded_movie_id])

    mse = mean_squared_error(y_pred.reshape(-1), y_test.rating.values)

    _mlflow.log_metrics({"test_mse": mse, "test_rmse": mse ** (0.5)})
