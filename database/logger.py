import datetime


def create_log(error: str, **kwargs) -> None:
    time: datetime.datetime = datetime.datetime.now()

    with open(f"./database/logs/{time.strftime('%d-%m-%Y_%H-%M-%S')}.txt", 'w') as log_file:
        log_file.write(f"{datetime.datetime.now()}\n")
        log_file.write(f"Error: {error}\n\n")
        log_file.write(f"Arguments:\n")

        for key, value in kwargs.items():
            log_file.write(f'{key}: {value}\n')
        log_file.close()

        return None