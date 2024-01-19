import logging
import os
import sys
import json
import argparse
from datetime import datetime
from os.path import normpath, basename

sys.path.append("./")  # Ensure src directory is accessible
from src.utils.utils import extract_dict_structure, split_in_sessions

USER_TAG = "[me]"
OTHERS_TAG = "[others]"


def save_messages_parsed(output_path, user_messages):
    output_file = os.path.join(output_path, "google-chats.txt")
    with open(output_file, 'w') as f:
        [f.write(f"{msg}\n") for msg in user_messages]



def messages_parser(google_chat_data, session_info: dict):
    datetime_format = "%A, %B %d, %Y at %I:%M:%S %p %Z"  # Adjust for Google Chat's timestamp format
    usr_id = 'user' + str(google_chat_data['me']['name'])  # Extract user ID
    usr_messages = []


    


    for message in google_chat_data['messages']:
        t_current = datetime.strptime(message['created_date'], datetime_format)
        split_in_sessions(t_current, None, usr_messages, session_info['delta_h_threshold'], session_info['session_token'])
        msg_prefix = USER_TAG if message['creator']['name'] == usr_id else OTHERS_TAG
        usr_messages.append(f"{msg_prefix} {message['text']}")
        

    return usr_messages

def load_data(json_path):
    with open(json_path, 'r') as f:
        google_chat_data = json.load(f)
    return google_chat_data  # No need to extract structure here

def main(argv):
    parser = argparse.ArgumentParser(prog=argv[0])
    parser.add_argument('--json_path', type=str, required=True,
                        help="Path to the JSON file containing Google Chat data")
    parser.add_argument('--output_path', type=str, default="./data/google_chat_parsed/",
                        help="Directory to save parsed messages")
    parser.add_argument('--personal_chat', type=bool, default=False,
                        help="Include the telegram personal chats. Default is disabled.")
    parser.add_argument('--session_token', type=str,
                        help="Add a 'session_token' after 'delta_h_threshold' hours"
                             "are elapsed between two messages. This allows splitting in sessions"
                             "one chat based on messages timing.")
    parser.add_argument("--delta_h_threshold", type=int, default=4,
                        help="Hours between two messages to before add 'session_token'")
    parser.add_argument("--time_format", type=str, default="%d-%m-%Y %H:%M:%S",
                    help="The timestamp format. Default is Indian format.")

    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    args = parser.parse_args(argv[1:])
    process_name = basename(normpath(argv[0]))
    logging.basicConfig(format=f"[{process_name}][%(levelname)s]: %(message)s", level=loglevel, stream=sys.stdout)
    delattr(args, "verbose")
    run(**vars(args))
    # ... (rest of the code)


# ... (Import, run, and main functions remain the same)
if __name__ == '__main__':
    main(sys.argv)
