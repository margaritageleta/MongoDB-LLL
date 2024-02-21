import json

from utils import parse_ssh_date_time, convert_ssh_to_human_readable


def return_file_contents(filename: str):
    file_contents = open(filename, mode='r')
    return file_contents.readlines()


def parse_ssh_log_file_file(filename: str, output_dir: str):
    ssh_log_file = return_file_contents(filename)
    log_dict = {}
    for lines in ssh_log_file:
        removed_line = lines.strip().replace('LabSZ', '').replace('pam_unix(sshd:auth): ', '').split('sshd')
        date_value = parse_ssh_date_time(removed_line[0].strip())
        log_text = f"{removed_line[1][8:]}\n"
        dict_key = convert_ssh_to_human_readable(date_value)
        if 'BREAK-IN' in log_text:
            if dict_key not in log_dict.keys():
                log_dict[dict_key] = [log_text]
            else:
                log_dict[dict_key].append(log_text)
        else:
            continue
    for key in log_dict.keys():
        op_file_fd = open(f"{output_dir}/{key}.log", 'w')
        op_file_fd.writelines(log_dict[key])


if __name__ == "__main__":
    parse_ssh_log_file_file(filename='dataset/ssh/ssh.log', output_dir='./dataset/ssh/break_in')
