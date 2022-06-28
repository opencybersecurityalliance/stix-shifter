import sys
from os import path
import re
from datetime import datetime
# from argparse import ArgumentParser

current_dir = path.abspath(path.dirname(__file__))
GITHUB_PR_PATH = "https://github.com/opencybersecurityalliance/stix-shifter/pull/"

CHANGE_LOG_PATH = path.abspath(path.join(current_dir, '../../../CHANGELOG.md'))
# CHANGE_LOG = path.abspath(path.join(CHANGE_LOG_PATH, "CHANGELOG.md"))
change_log_file = open(CHANGE_LOG_PATH, "a")

# old_change_log = change_log_file.read()
# print(old_change_log)


def __main__():
    
    git_logs = sys.argv[1]
    release_tag = sys.argv[2]
    time = datetime.now()
    log_list = "## {} ({})\n\n### Breaking changes:\n\n### Deprecations:\n\n### Changes:\n\n".format(release_tag, time.strftime("%Y-%m-%d"))
    ending = "\n\n--------------------------------------\n\n"
    git_logs = __format_logs(git_logs)

    try: 
        log_list = log_list + git_logs + ending
        change_log_file.write(log_list)
        change_log_file.close()
    except ValueError as ex:
        print(ex)

# def __line_prepender(filename, line):
#     with open(filename, 'r+') as f:
#         content = f.read()
#         f.seek(0, 0)
#         f.write(line.rstrip('\r\n') + '\n' + content)

def __format_logs(logs):
    logs_list = logs.split("\n")
    commit_hash_pattern = "^.{8}"
    open_parenth_pattern = "\((?=#.{3})"
    close_parenth_pattern = "\)$" 
    updated_logs = ""
    
    for lg in logs_list:
        lg = re.sub(commit_hash_pattern, "*", lg)
        lg = re.sub(open_parenth_pattern, "[", lg)
        lg = re.sub(close_parenth_pattern, "]", lg)
        pr_id = re.search("#\d{3,4}]$", lg)[0]
        pr_id = re.sub("]$", "", pr_id)
        pr_id = re.sub("#", "", pr_id)
        lg = lg + "(" + GITHUB_PR_PATH + pr_id + ")"
        updated_logs = updated_logs + lg + "\n"

    return updated_logs


if __name__ == "__main__":
    __main__()