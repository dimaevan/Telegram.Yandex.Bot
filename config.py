import yaml


def data_config():
    with open("config.yaml", 'r') as file_config:
        return yaml.safe_load(file_config)


if __name__ == "__main__":
    print(data_config())