# Caml
## Installation
Use the package manager `pip` to install `caml`.

```
pip install git+https://github.com/tronglh241/caml.git@dev
```

## Setup ClearML
1. Access your ClearML WebUI with the provided account. On the `SETTINGS > WORKSPACE` page, click Create new credentials > Copy to clipboard.
The credentials should look like this.
    ```
    api {
        web_server: http://localhost:8080
        api_server: http://localhost:8008
        files_server: http://localhost:8081
        credentials {
            "access_key" = "TMV625WHMGQGNZYX..."
            "secret_key" = "56mdkBzZ1mwQ2F114J0m6Fke8WKvQs1Fi7dooJijUoLjsJ3..."
        }
    }
    ```
1. Open a terminal, and run `clearml-init` to set up ClearML on your local machine. At the command prompt `Paste copied configuration here:`, copy and paste the credentials that you have created.
1. Enter the ClearML Server web server URL (the text after `web_server` in the credentials (`http://localhost:8080`)).
1. Enter the ClearML Server API server URL (the text after `api_server` in the credentials (`http://localhost:8008`)).
1. Enter the ClearML Server file server URL (the text after `files_server` in the credentials (`http://localhost:8081`)).
1. Console will show where the config is stored.

    ```
    Verifying credentials ...
    Credentials verified!

    New configuration stored in /home/<username>/clearml.conf
    CLEARML setup completed successfully.
    ```
    Open that config file, and check if `web_server`, `api_server`, and `api_server` are appropriately configured.

## Usage
### Initialize a project
1. To start a new project, run `caml init <project_dir>`. This will generate a folder in the current working directory having the following structure:

    ```
    project/
    ├── config
    │   ├── eval.yml
    │   ├── query.yml
    │   └── train.yml
    ├── dataset.py
    ├── model.py
    ├── requirements.txt
    └── run.py
    ```
1. Change directory to `project_dir`, and initialize `git`.
    ```
    git init
    git remote add origin <remote-url>
    ```

### Structure details
1. `dataset.py` is where you define your dataset class. There are 3 unimplemented methods:
    - `load_dataset`: loads dataset from `path` into `self` for returning samples `X` and targets `y`.
    - `X`: returns a list of samples.
    - `y`: returns a list of targets.
1. `model.py` is where you define your train model and eval model.
    1. `TrainModel`:
        - `fit`: receives samples `X` and targets `y` from the dataset, then trains the model.
        - `best_model`: returns the path to your best-trained model/checkpoint.
        - `load_model`: loads a model/checkpoint from a path.
    1. `EvalModel`:
        - `predict`: makes predictions for samples `X`.
        - `predict_proba`: returns probabilities of input, it should be a list of `np.ndarray` having the shape of `1xn`.
        - `eval`: receives `pred` from `predict` and targets `y`, and returns a tuple of `(metric_name, metric_value)`
        - `load_model`: loads a model/checkpoint from a path.
1. `requirements.txt` is where you put all the dependencies needed for the project.
1. `config` is where you define configs for `query`, `train`, and `eval`.
      - `project_name`, `task_name`: will be shown on WebUI.
      - `remote`: specifies whether to run on ClearML Agent or not.
      - `queue_name`: In case `remote` is True, the task will execute on queue `queue_name`.
      - Any key ending up with `_conf` must have the form:
        ```
        module: <module_name>
        name: <name>
        kwargs:
        ⠀⠀key: value
        ⠀⠀...
        ```
        This is interpreted as:
        ```
        def func():
        ⠀⠀from module_name import name
        ⠀⠀return name(**kwargs)
        ```

### Execution
After implementing `dataset.py`, `model.py` and configuring `config`, you can `query`, `train`, and `eval` by running:

- Query: `python run.py query`
- Train: `python run.py train`
- Eval: `python run.py eval`
