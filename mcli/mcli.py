"""
Simple command-line interface to music service
"""

# Standard library modules
import argparse
import cmd
import re
from subprocess import run, PIPE

# Installed packages
import requests

# The services check only that we pass an authorization,
# not whether it's valid
DEFAULT_AUTH = 'Bearer A'


def parse_args():
    argp = argparse.ArgumentParser(
        'mcli',
        description='Command-line query interface for all microservices'
        )
    # argp.add_argument(
    #     'name',
    #     help="DNS name or IP address of microservice"
    #     )
    # argp.add_argument(
    #     'port',
    #     type=int,
    #     help="Port number of microservice"
    #     )
    # argp.add_argument(
    #     'microservice',
    #     help="Microservice type"
    # )
    return argp.parse_args()


def get_url(name, port,mode):
# , microservice):
    return "http://{}:{}/api/v1/{}/".format(name, port,mode)
    # , microservice)


def parse_quoted_strings(arg):
    """
    Parse a line that includes words and '-, and "-quoted strings.
    This is a simple parser that can be easily thrown off by odd
    arguments, such as entries with mismatched quotes.  It's good
    enough for simple use, parsing "-quoted names with apostrophes.
    """
    mre = re.compile(r'''(\w+)|'([^']*)'|"([^"]*)"''')
    args = mre.findall(arg)
    return [''.join(a) for a in args]


class Mcli(cmd.Cmd):
    def __init__(self, args):
        self.mode = input("Enter service mode:")
        # self.name = args.name
        # self.port = args.port
        # self.microservice = args.microservice
        cmd.Cmd.__init__(self)
        self.prompt = 'ql: '
        self.maps = {
            'user': {'host': '172.17.0.6', 'port': '30002'},
            'music': {'host': '172.17.0.4', 'port': '30001'}
        }
        self.intro = """
Command-line interface to all microservices.
Enter 'help' for command list.
'Tab' character autocompletes commands.
"""

    def do_read(self, arg):
        """
        Read a single song or list all songs.

        Parameters
        ----------
        song:  music_id (optional)
            The music_id of the song to read. If not specified,
            all songs are listed.

        Examples
        --------
        read 6ecfafd0-8a35-4af6-a9e2-cbd79b3abeea
            Return "The Last Great American Dynasty".
        read
            Return all songs (if the server supports this).

        Notes
        -----
        Some versions of the server do not support listing
        all songs and will instead return an empty list if
        no parameter is provided.
        """
        # print(arg)
        url = get_url(self.maps[self.mode]['host'], self.maps[self.mode]['port'], self.mode)
        if(self.mode == "music"):
            # , self.microservice)
            print(self.maps)
            # if self.microservicxe == 'music':
            r = requests.get(
                url+arg.strip(),
                headers={'Authorization': DEFAULT_AUTH}
                )
            if r.status_code != 200:
                print("Non-successful status code:", r.status_code)
            items = r.json()
            if 'Count' not in items:
                print("0 items returned")
                return
            print("{} items returned".format(items['Count']))
            for i in items['Items']:
                print("{}  {:20.20s} {}".format(
                    i['music_id'],
                    i['Artist'],
                    i['SongTitle']))

        elif(self.mode == "user"):
            r = requests.get(
                url+arg.strip(),
                headers={'Authorization': DEFAULT_AUTH}
                )
            if r.status_code != 200:
                print("Non-successful status code:", r.status_code)
            print("CONTENT", r.content)
            items = r.json()
            if 'Count' not in items:
                print("0 items returned")
                return
            print("{} items returned".format(items['Count']))
            for i in items['Items']:
                print("{} {} {} {}".format(
                    i['user_id'],
                    i['email'],
                    i['fname'],
                    i['lname']))
    
    def do_changeMode(self, arg):
        self.mode = arg.strip().split(' ')[-1]


    def do_create(self, arg):
        """
        Add a song to the database.

        Parameters
        ----------
        artist: string
        title: string

        Both parameters can be quoted by either single or double quotes.

        Examples
        --------
        create 'Steely Dan'  "Everyone's Gone to the Movies"
            Quote the apostrophe with double-quotes.

        create Chumbawamba Tubthumping
            No quotes needed for single-word artist or title name.
        """
        url = get_url(self.name, self.port)
        args = parse_quoted_strings(arg)
        payload = {
            'Artist': args[0],
            'SongTitle': args[1]
        }
        r = requests.post(
            url,
            json=payload,
            headers={'Authorization': DEFAULT_AUTH}
        )
        print(r.json())

    def do_delete(self, arg):
        """
        Delete a song.

        Parameters
        ----------
        song: music_id
            The music_id of the song to delete.

        Examples
        --------
        delete 6ecfafd0-8a35-4af6-a9e2-cbd79b3abeea
            Delete "The Last Great American Dynasty".
        """
        url = get_url(self.name, self.port)
        r = requests.delete(
            url+arg.strip(),
            headers={'Authorization': DEFAULT_AUTH}
            )
        if r.status_code != 200:
            print("Non-successful status code:", r.status_code)

    def do_quit(self, arg):
        """
        Quit the program.
        """
        return True

    def do_test(self, arg):
        """
        Run a test stub on the music server.
        """
        url = get_url(self.name, self.port)
        r = requests.get(
            url+'test',
            headers={'Authorization': DEFAULT_AUTH}
            )
        if r.status_code != 200:
            print("Non-successful status code:", r.status_code)

    def do_shutdown(self, arg):
        """
        Tell the music cerver to shut down.
        """
        url = get_url(self.name, self.port)
        r = requests.get(
            url+'shutdown',
            headers={'Authorization': DEFAULT_AUTH}
            )
        if r.status_code != 200:
            print("Non-successful status code:", r.status_code)


if __name__ == '__main__':
    args = parse_args()
    Mcli(args).cmdloop()
