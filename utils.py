from datetime import datetime

def parse_ssh_date_time(time_entry: str):

    ssh_date_time = datetime.strptime(time_entry, "%b %d %H:%M:%S")

    if ssh_date_time.month == "12":
        ssh_date_time = ssh_date_time.replace(year=2016)
    else:
        ssh_date_time = ssh_date_time.replace(year=2017)

    return ssh_date_time


def convert_ssh_to_human_readable(time_entry: datetime):
    return f"{time_entry.day}_{time_entry.month}_{time_entry.year}"


if __name__ == '__main__':
    print(parse_ssh_date_time("Dec 13 02:25:30"))
