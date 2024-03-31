from pureml.components import dataset
from rich import print



def get_dataset_helper(label_dataset):
    dataset_label = dataset.fetch(label_dataset)

    if dataset_label is None:
        print("[orange] Unable to fetch the dataset")
        return None
    else:
        print("[green] Succesfully fetched the dataset")
        return dataset_label