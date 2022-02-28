from datetime import datetime


def format_date(date):
    return datetime.fromtimestamp(date).strftime("%d %B %Y %I:%M:%S")


if __name__ == "__main__":
    print(format_date(1646046237))
