class DQNConfig():

    config = {
        "game" : {
            "board_size" : 9,
            "nb_futur_states" : 140, #12 + 2*(board_size-1)**2
            "nb_walls" : 20
        },

        "model" : {
            "input_weight" : "dqn_weight.h5",
            "output_weight" : "updated_weight",
            "kernel size" : 3,
            "nb_channels" : [],
            "mlp_size" : []

        },

        "learning": {
            "eps" : 1,
            "eps_decay" : 0.99,
            "eps_min" : 0.1,
            "gamma" : 0.9,
            "lr" : 1e-3,
            "nb_samples_to_train" : 10000,
            "nb_training" : 10000,
            "batch_size" : 64
        }

    }