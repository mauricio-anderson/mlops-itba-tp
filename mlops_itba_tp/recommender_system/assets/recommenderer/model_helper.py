""" """
from tensorflow.keras import layers
from tensorflow.keras import Model


def get_model(n_movies, n_users, n_latent_factors) -> Model:
    """ """

    # Input layer
    movie_input = layers.Input(shape=[1], name='Item')
    user_input = layers.Input(shape=[1],name='User')

    # Movies
    movie_embedding = layers.Embedding(
        n_movies + 1,
        n_latent_factors,
        mask_zero=True,
        name='Movie-Embedding'
    )(movie_input)

    movie_vec = layers.Flatten(name='FlattenMovies')(movie_embedding)

    # Users
    user_embedding = layers.Embedding(
            n_users + 1,
            n_latent_factors,
            mask_zero=True,
            name='User-Embedding'
    )(user_input)

    user_vec = layers.Flatten(name='FlattenUsers')(user_embedding)

    # Dot product
    prod = layers.Dot(axes=1, name='DotProduct')([movie_vec, user_vec])

    # Model
    model = Model([user_input, movie_input], prod)

    return model
