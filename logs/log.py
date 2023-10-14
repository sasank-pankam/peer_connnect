import datetime


def __getTimeStamp() -> str:
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

    return formatted_datetime


def writeLogMainServer(message: str):
    time = __getTimeStamp()
    with open('log_files/server.log', 'a') as log_file:
        log_file.write(f'[ {time} ]  -> {message} ')


def writeLogFileSharingErrors(message: str):
    time = __getTimeStamp()
    with open('log_files/file_sharing_errors.log', 'a') as log_file:
        log_file.write(f'[ {time} ]  -> {message} ')


def writeLogTextTransferErrors(message: str):
    time = __getTimeStamp()
    with open('log_files/text_transfer.log', 'a') as log_file:
        log_file.write(f'[ {time} ]  -> {message} ')


def writeLogPeerConnectionErrors(message: str):
    time = __getTimeStamp()
    with open('log_files/peer_connection.log', 'a') as log_file:
        log_file.write(f'[ {time} ]  -> {message} ')


if __name__ == '--main__':
    pass
