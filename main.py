import hashlib
import os
import tailer

# Get the home directory of the current user
home_dir = os.path.expanduser('~')

# Construct paths dynamically
cache_dir = os.path.join(home_dir, 'lancache/lancache/cache/cache')
log_file_path = os.path.join(home_dir, 'lancache/lancache/logs/access.log')

class LineManager:
    lines = ['a', 'b', 'c', 'd', 'e']

    def addLine(self, line: str):
        # Split the line into segments
        split_line = line.split(' ')

        # Check if line is related to steam or epicgames
        if split_line[0] not in ['[steam]', '[epicgames]']:
            return

        # Apply specific checks for steam or epicgames
        if split_line[0] == '[steam]':
            # Ignore Server Status for steam
            if split_line[9] == '/server-status':
                return
            # Ignore Steam Client
            if split_line[9] == '/client/steam_client_win32':
                return
        elif split_line[0] == '[epicgames]':
            # Add specific checks for epicgames if needed here
            pass

        # Append the file path to our list
        self.lines.append(split_line[9])

        # Ensure there are only ever 5 elements in the list
        if len(self.lines) > 5:
            self.lines.pop(0)

    def isListSame(self):
        # Check if all elements in the list are identical
        if len(set(self.lines)) == 1:
            # Get the corrupted file
            line = self.lines[0]

            # Reset the list
            self.regenList()

            # Return the corrupted file
            return [True, line]
        return [False, '']

    def regenList(self):
        # Reset the list to its default values
        self.lines = ['a', 'b', 'c', 'd', 'e']

    def printList(self):
        # Print the current list of lines
        for line in self.lines:
            print(line)

def deleteFile(path, platform):
    # Adjust the prefix based on the platform
    prefix = 'steam' if platform == '[steam]' else 'epicgames'
    
    # Create our hash string
    hash_string = prefix + path + 'bytes=0-1048575'

    # Hash our string
    string_hash = hashlib.md5(hash_string.encode()).hexdigest()

    # Create Absolute Path dynamically based on user's home directory
    absolute_path = os.path.join(cache_dir, string_hash[-2:], string_hash[-4:-2], string_hash)

    # Delete File
    if os.path.isfile(absolute_path):
        os.remove(absolute_path)

if __name__ == '__main__':
    # Create the Line Manager
    line_manager = LineManager()

    # Listen to Access Log
    for tail_line in tailer.follow(open(log_file_path)):
        # Determine platform based on line content
        platform = '[steam]' if '[steam]' in tail_line else '[epicgames]' if '[epicgames]' in tail_line else None

        # Add Line if it belongs to steam or epicgames
        if platform:
            line_manager.addLine(tail_line)

            # Check if there is a corrupted file in the cache
            list_is_same = line_manager.isListSame()

            # Delete File based on the platform
            if list_is_same[0]:
                print(list_is_same[1] + " is corrupted. Purging from cache.")
                deleteFile(list_is_same[1], platform)
