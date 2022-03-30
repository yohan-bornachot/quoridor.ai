class DQNConfig():

    config = {
        "game" : {
            "board_size" : 9,
            "nb_futur_states" : 140, #12 + 2*(board_size-1)**2
            "nb_walls" : 20
        },

        "model" : {
            "input_weight" : None,
            "output_weight" : "updated_weight/",
            "kernel_size" : 3,
            "nb_channels" : [10, 20],
            "mlp_size" : [88, 100, 120]

        },

        "learning": {
            "eps" : 1,
            "eps_decay" : 0.95,
            "eps_min" : 0.1,
            "gamma" : 0.9,
            "lr" : 1e-3,
            "nb_samples_to_train" : 10000,
            "nb_training" : 100,
            "batch_size" : 64
        }

    }