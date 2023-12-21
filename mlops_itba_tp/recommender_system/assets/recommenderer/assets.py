""" """
import os
import numpy as np
from sklearn.metrics import mean_squared_error
from dagster import asset, AssetIn, Int, Float, multi_asset, AssetOut
from dagster_mlflow import mlflow_tracking
import pandas as pd
from typing import Dict, Tuple
from sklearn.model_selection import train_test_split
from tensorflow.keras import Model
from matplotlib import pyplot as plt

from mlops_itba_tp.recommender_system.assets.recommenderer.model_helper import get_model
from keras.optimizers import Adam

mlflow = mlflow_tracking.configured({
    "experiment_name": "recommender-system",
    "mlflow_tracking_uri": os.environ["MLFLOW_TRACKING_URI"],
})


@multi_asset(
    ins={
        "upstream": AssetIn("training_data")
    },
    outs={
        "preprocessed_training_data": AssetOut(),
        "user2Idx": AssetOut(),
        "movie2Idx": AssetOut(),
    }
)
def preprocess_data(context, upstream: pd.DataFrame) -> Tuple[pd.DataFrame, Dict, Dict]:
    """ """
    training_data = upstream

    u_unique = training_data.user_id.unique()
    user2Idx: Dict = {o:i+1 for i,o in enumerate(u_unique)}

    m_unique = training_data.movie_id.unique()
    movie2Idx: Dict = {o:i+1 for i,o in enumerate(m_unique)}

    training_data['encoded_user_id'] = training_data.user_id.apply(lambda x: user2Idx[x])
    training_data['encoded_movie_id'] = training_data.movie_id.apply(lambda x: movie2Idx[x])

    preprocessed_training_data: pd.DataFrame = training_data.copy()

    return preprocessed_training_data, user2Idx, movie2Idx


@multi_asset(
    ins={
        "preprocessed_training_data": AssetIn()
    },
    outs={
        "X_train": AssetOut(),
        "X_test": AssetOut(),
        "y_train": AssetOut(),
        "y_test": AssetOut(),
    }
)
def split_data(context, preprocessed_training_data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """ """
    test_size=0.10
    random_state=42
    X_train, X_test, y_train, y_test = train_test_split(
        preprocessed_training_data[['encoded_user_id', 'encoded_movie_id']],
        preprocessed_training_data[['rating']],
        test_size=test_size,
        random_state=random_state
    )
    return X_train, X_test, y_train, y_test


@asset(
    resource_defs={
        'mlflow': mlflow
        },
    ins={
        "X_train": AssetIn(),
        "y_train": AssetIn(),
        "user2Idx": AssetIn(),
        "movie2Idx": AssetIn(),
    },
    config_schema={
        'batch_size': Int,
        'epochs': Int,
        'learning_rate': Float,
        'embeddings_dim': Int
    }
)
def keras_dot_product_model(context, X_train, y_train, user2Idx, movie2Idx) -> Model:
    """ """

    mlflow = context.resources.mlflow

    mlflow.log_params(context.op_config)

    # Model hyperparameters
    batch_size = context.op_config["batch_size"]
    epochs = context.op_config["epochs"]
    learning_rate = context.op_config["learning_rate"]
    embeddings_dim = context.op_config["embeddings_dim"]

    # Model
    model = get_model(len(movie2Idx), len(user2Idx), embeddings_dim)
    model.compile(Adam(learning_rate=learning_rate), 'mean_squared_error')

    # Model training
    context.log.info(f'batch_size: {batch_size} - epochs: {epochs}')
    history = model.fit(
        [
            X_train.encoded_user_id,
            X_train.encoded_movie_id
        ],
        y_train.rating,
        batch_size=batch_size,
        # validation_data=([ratings_val.userId, ratings_val.movieId], ratings_val.rating),
        epochs=epochs,
        verbose=1
    )

    # Log mlflow data
    for i, l in enumerate(history.history['loss']):
        mlflow.log_metric('mse', l, i)

    # fig, axs = plt.subplots(1)
    # axs.plot(history.history['loss'], label='mse')
    # plt.legend()
    # mlflow.log_figure(fig, 'plots/loss.png')

    return model


@asset(
    resource_defs={'mlflow': mlflow},
    ins={
        "keras_dot_product_model": AssetIn(),
    },
    name="model_data"
)
def log_model(context, keras_dot_product_model: Model) -> Dict:
    """ """
    mlflow = context.resources.mlflow

    logged_model = mlflow.tensorflow.log_model(
        keras_dot_product_model,
        "keras_dot_product_model",
        registered_model_name='keras_dot_product_model',
        input_example=[np.array([1, 2]), np.array([2, 3])],
    )

    model_data = {
        'model_uri': logged_model.model_uri,
        'run_id': logged_model.run_id
    }

    return model_data


@asset(
    resource_defs={'mlflow': mlflow},
    ins={
        "model_data": AssetIn(),
        "X_test": AssetIn(),
        "y_test": AssetIn(),
    }
)
def evaluate_model(context, model_data, X_test, y_test) -> None:
    """ """

    mlflow = context.resources.mlflow

    logged_model = model_data['model_uri']

    loaded_model = mlflow.pyfunc.load_model(logged_model)

    y_pred = loaded_model.predict([
        X_test.encoded_user_id,
        X_test.encoded_movie_id
    ])

    mse = mean_squared_error(
        y_pred.reshape(-1),
        y_test.rating.values
        )

    mlflow.log_metrics({
        'test_mse': mse,
        'test_rmse': mse**(0.5)
    })

