import praw
import getpass
from praw.models import Submission
from praw.models import Comment

def get_instance():
    username = input("username=")
    password = getpass.getpass()
    client_id = input("client_id=")
    client_secret = input("client_secret=")
    return praw.Reddit(client_id=client_id, client_secret=client_secret, password=password, user_agent=username, username=username)

try:
    order = input('Keep correct order of saved items? [Y/n]')
except SyntaxError:
    order = None

print("Login to old Account")
old_account = get_instance()

print("Login to new Account")
new_account = get_instance()

print('Getting list of saved items from old Account')

saved = old_account.user.me().saved(limit=None)

reversed_list = []

for item in saved:
    if isinstance(item, Submission):
        reversed_list.append('Submission {}'.format(item))
    else:
        reversed_list.append('Comment {}'.format(item))
        print('Comment {}'.format(item))

if order == 'Y' or order == None:
    reversed_list.reverse()

for item in reversed_list:
    if item.startswith('Comment'):
        item_id = item.replace("Comment ", "")
        print('Saving comment {}'.format(item_id))
        new_account.comment(id=item_id).save()
    else:
        item_id = item.replace("Submission ", "")
        print('Saving submission {}'.format(item_id))
        new_account.submission(id=item_id).save()
