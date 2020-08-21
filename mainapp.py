"""
Welcome to Library CLI.

***********************************************  VERY IMPORTANT  ***********************************************
This application utilizes a command line interface to work with ebooks and files. Though such a task is very difficult
through a CLI, the true purpose of this application is practice for its author to use SQL and SQLite3 in python in
preparation of using the algorithms built here for a GUI application which has the same purpose.
*********************************************************************************************************************

The following application has relatively very few commands but each command has its own share of arguments.
The commands are:
-add
-del
-getid
-open
-reset
-search
-update

These commands look or sound similar to SQL commands and that is because they are intentionally designed that way.
Find the documentation of each below.

The application connects to a database "ebooks.db" or creates one if it does not exist and creates a table called
ebooks.

There are 5 fields:
Name
Author
Path
Genre
Folder

You can work with the values of these fields using the commands above.

Note: no parameters but "specified value" means that there will be input() following.
"""
import sqlite3
import cmd
import os
from glob import glob
from colorama import init, Fore
init(autoreset=True)


# noinspection PyUnusedLocal
class App(cmd.Cmd):
    intro = "Welcome to Library CLI"
    prompt = ">>>"
    file = None
    db = "./ebooks.db"

    def __init__(self):
        """
        Connects to ebooks.db or creates it if it is not there.
        It will also create a table or pass if the table is there.
        """
        super().__init__()
        self.conn = sqlite3.connect(self.db)
        self.c = self.conn.cursor()
        try:
            self.c.execute("""CREATE TABLE ebooks (
                              name TEXT,
                              author TEXT,
                              path TEXT,
                              folder TEXT,
                              genre TEXT
            );""")
        except sqlite3.Error:
            pass

    def do_add(self, arg):
        """
        Add a directory of ebooks or an ebook.

        Arg:         Param:                 Function:
        dir          <recur/nrecur>         adds all the files in a single directory
        book         none                   adds a book with specified values


        Name    > Must not be identical to any other name.
        Path    > Must be absolute path to the file.

        add dir recur                       adds all files in directory and subdirectory
        add dir nrecur                      adds all files in directory only
        """
        try:
            array = arg.split()
            if array[0] == "book":
                name = input(f"{Fore.BLUE}Name: ")
                path = input(f"{Fore.BLUE}Path: ")
                folder = input(f"{Fore.BLUE}Folder: ")
                author = input(f"{Fore.BLUE}Author: ")
                genre = input(f"{Fore.BLUE}Genre: ")
                self.addbook(name, author, path, folder, genre)
            elif array[0] == "dir":
                directory = input(f"{Fore.BLUE}Path: ")
                if array[1] == "recur":
                    self.add_dir_files(directory, True)
                elif array[1] == "nrecur":
                    self.add_dir_files(directory, False)
                else:
                    print(f"{Fore.RED}Input a correct argument.")
            else:
                return print(f"{Fore.RED}Input a correct argument.")
            print(f"{Fore.GREEN}Operation Successful.")
        except Exception as e:
            print(f"{Fore.RED}{e}")

    def do_getid(self, arg):
        """
        Retrieve the ID of a book by using its name.

        No arguments.
        """
        try:
            name = input(f"{Fore.BLUE}Name: ")
            self.getid(name)
        except Exception as e:
            print(f"{Fore.RED}{e}")

    def do_update(self, arg):
        """Update the information based on the specified criteria.

        Arg:         Param:                 Function:
        name         none                   updates the ebook of specified name with new value
        folder       none                   updates all ebooks of specified folder with new value
        author       none                   updates all ebooks of specified author with new value
        genre        none                   updates all ebooks of specified genre with new value


        Optional Arg:
        update ebook <rowid> <name,folder,genre,author>

        This is used to update a specific field of a specific ebook.

        Ex: update ebook 1 name
        You will then input the new name.
        """
        try:
            array = arg.split()
            if array[0] == "name":
                old_name = input(f"{Fore.BLUE}Old Name: ")
                new_name = input(f"{Fore.BLUE}New Name: ")
                with self.conn:
                    self.c.execute("UPDATE ebooks SET name=:new_name WHERE name=:old_name",
                                   {"new_name": new_name, "old_name": old_name})
            elif array[0] == "author":
                old_author = input(f"{Fore.BLUE}Old Author: ")
                new_author = input(f"{Fore.BLUE}New Author: ")
                with self.conn:
                    self.c.execute("UPDATE ebooks SET author=:new_author WHERE author=:old_author",
                                   {"new_author": new_author, "old_author": old_author})
            elif array[0] == "folder":
                old_folder = input(f"{Fore.BLUE}Old Folder: ")
                new_folder = input(f"{Fore.BLUE}New Folder: ")
                with self.conn:
                    self.c.execute("UPDATE ebooks SET folder=:new_folder WHERE folder=:old_folder",
                                   {"new_folder": new_folder, "old_folder": old_folder})
            elif array[0] == "genre":
                old_genre = input(f"{Fore.BLUE}Old Genre: ")
                new_genre = input(f"{Fore.BLUE}New Genre: ")
                with self.conn:
                    self.c.execute("UPDATE ebooks SET genre=:new_genre WHERE genre=:old_genre",
                                   {"new_genre": new_genre, "old_genre": old_genre})
            elif array[0] == "ebook":
                rowid = int(array[1])
                self.info(rowid)
                if array[2] == "name":
                    new_name = input(f"{Fore.BLUE}New Name: ")
                    with self.conn:
                        self.c.execute("UPDATE ebooks SET name=:new_name WHERE rowid=:rowid",
                                       {"new_name": new_name, "rowid": rowid})
                elif array[2] == "author":
                    new_author = input(f"{Fore.BLUE}New Author: ")
                    with self.conn:
                        self.c.execute("UPDATE ebooks SET author=:new_author WHERE rowid=:rowid",
                                       {"new_author": new_author, "rowid": rowid})
                elif array[2] == "folder":
                    new_folder = input(f"{Fore.BLUE}New Folder: ")
                    with self.conn:
                        self.c.execute("UPDATE ebooks SET folder=:new_folder WHERE rowid=:rowid",
                                       {"new_folder": new_folder, "rowid": rowid})
                elif array[2] == "genre":
                    new_genre = input(f"{Fore.BLUE}New Genre: ")
                    with self.conn:
                        self.c.execute("UPDATE ebooks SET genre=:new_genre WHERE rowid=:rowid",
                                       {"new_genre": new_genre, "rowid": rowid})
                else:
                    print(f"{Fore.RED}Specify a proper argument.")
            else:
                return print(f"{Fore.RED}Specify a proper argument.")
            print(f"{Fore.GREEN}Operation Successful.")
        except Exception as e:
            print(f"{Fore.RED}{e}")

    def do_search(self, arg):
        """Search for ebooks based on specified criteria.

        Arg:         Param:                 Function:
        id           <rowid>                searches the ebook with that id
        name         none                   searches the ebook with specified name
        folder       none                   searches all ebooks with specified folder
        author       none                   searches all ebooks with specified author
        genre        none                   searches all ebooks with specified genre
        """
        try:
            array = arg.split()
            if array[0] == "id":
                with self.conn:
                    self.c.execute("SELECT * FROM ebooks WHERE rowid=:id", {"id": int(array[1])})
                    book_list = self.c.fetchall()
                    self.display(book_list)
            elif array[0] == "name":
                name = input(f"{Fore.BLUE}Name: ")
                with self.conn:
                    self.c.execute("SELECT * FROM ebooks WHERE name=:name", {"name": name})
                    book_list = self.c.fetchall()
                    self.display(book_list)
            elif array[0] == "folder":
                folder = input(f"{Fore.BLUE}Folder: ")
                with self.conn:
                    self.c.execute("SELECT * FROM ebooks WHERE folder=:folder", {"folder": folder})
                    book_list = self.c.fetchall()
                    self.display(book_list)
            elif array[0] == "author":
                author = input(f"{Fore.BLUE}Author: ")
                with self.conn:
                    self.c.execute("SELECT * FROM ebooks WHERE author=:author", {"author": author})
                    book_list = self.c.fetchall()
                    self.display(book_list)
            elif array[0] == "genre":
                genre = input(f"{Fore.BLUE}Genre")
                with self.conn:
                    self.c.execute("SELECT * FROM ebooks WHERE genre=:genre", {"genre": genre})
                    book_list = self.c.fetchall()
                    self.display(book_list)
            else:
                return print(f"{Fore.RED}Specify proper argument.")
            print(f"{Fore.GREEN}Operation Successful.")
        except Exception as e:
            print(f"{Fore.RED}{e}")

    def do_open(self, arg):
        """
        Open the specified argument.


        Arg:         Param:                 Function:
        id           <rowid>                opens the ebook with that rowid
        name         none                   opens the ebook with specified name
        path         none                   opens the file/directory with specified path
        """
        try:
            array = arg.split()
            if array[0] == "id":
                with self.conn:
                    self.c.execute("SELECT path FROM ebooks WHERE rowid=:rowid", {"rowid": int(array[1])})
                    book = self.c.fetchone()[0]
                    os.startfile(book)
            elif array[0] == "name":
                name = input(f"{Fore.BLUE}Name: ")
                with self.conn:
                    self.c.execute("SELECT path FROM ebooks WHERE name=:name", {"name": name})
                    book = self.c.fetchone()[0]
                    os.startfile(book)
            elif array[0] == "path":
                path = input(f"{Fore.BLUE}Path: ")
                os.startfile(path)
            else:
                return print(f"{Fore.RED}Recheck your statement.")
            print(f"{Fore.GREEN}Operation Successful.")
        except Exception as e:
            print(f"{Fore.RED}{e}")

    def do_del(self, arg):
        """
        Deletes the specified argument.

        Arg:         Param:                 Function:
        id           <rowid>                deletes the ebook with that id
        name         none                   deletes the ebook with specified name
        folder       none                   deletes all ebooks with specified folder
        author       none                   deletes all ebooks with specified author
        genre        none                   deletes all ebooks with specified genre
        """
        try:
            array = arg.split()
            if array[0] == "id":
                with self.conn:
                    self.c.execute("DELETE FROM ebooks WHERE rowid=:id", {"id": int(array[1])})
            elif array[0] == "name":
                name = input(f"{Fore.BLUE}Name: ")
                with self.conn:
                    self.c.execute("DELETE FROM ebooks WHERE name=:name", {"name": name})
            elif array[0] == "folder":
                folder = input(f"{Fore.BLUE}Folder: ")
                with self.conn:
                    self.c.execute("DELETE FROM ebooks WHERE folder=:folder", {"folder": folder})
            elif array[0] == "author":
                author = input(f"{Fore.BLUE}Author: ")
                with self.conn:
                    self.c.execute("DELETE FROM ebooks WHERE author=:author", {"author": author})
            elif array[0] == "genre":
                genre = input(f"{Fore.BLUE}Genre: ")
                with self.conn:
                    self.c.execute("DELETE FROM ebooks WHERE genre=:genre", {"genre": genre})
            else:
                return print(f"{Fore.RED}Specify proper argument.")
            print(f"{Fore.GREEN}Operation Successful.")
        except Exception as e:
            print(f"{Fore.RED}{e}")

    def do_reset(self, arg):
        """
        Clears all records from the table.
        """
        with self.conn:
            self.c.execute("DELETE FROM ebooks;")
        print(f"{Fore.GREEN}All data in the database has been deleted.")

    def addbook(self, name, author, path, folder, genre):
        """
        Adds book to the table.
        User must have already inputted the arguments above.
        """
        with self.conn:
            self.c.execute("""INSERT INTO ebooks (name, path, folder, author, genre) 
                              VALUES (:name, :path, :folder, :author, :genre);""", {"name": name, "path": path,
                                                                                    "folder": folder, "author": author,
                                                                                    "genre": genre})
        print(f"{Fore.GREEN}Ebook added successfully.")

    def add_dir_files(self, path, rec):
        """
        Adds to the table all the files that are in a directory.
        Path of directory must be specified.
        Will add the ebook name and path only to the table.
        All other fields remain blank.
        """
        names = []
        if rec:
            files = glob(path + '/**/*.*', recursive=rec)
        else:
            files = glob(path + '/*.*', recursive=rec)
        for file in files:
            file = os.path.basename(file)
            name = os.path.splitext(file)[0]
            names.append(name)
        with self.conn:
            for name, path in zip(names, files):
                self.addbook(name, "", path, "", "")
        print(f"\n{Fore.GREEN}{len(files)} Ebooks Added\n")

    def getid(self, name):
        """
        Prints out the rowid of an ebook, and uses ebook's name as an argument.
        """
        with self.conn:
            self.c.execute("SELECT rowid FROM ebooks WHERE name = :name;", {"name": name})
            print(f"{Fore.BLUE}RowID of {name}: {Fore.GREEN}{self.c.fetchone()[0]}")

    def info(self, book_id):
        """
        Prints out the rowid, name, author, path, folder, and genre of the ebook with rowid=argument.
        """
        with self.conn:
            self.c.execute("SELECT * FROM ebooks WHERE rowid=:id", {"id": int(book_id)})
            book = self.c.fetchone()
            print("\n")
            print(f"{Fore.BLUE}ID: {Fore.GREEN}{book_id}")
            print(f"{Fore.BLUE}Name: {Fore.GREEN}{book[0]}")
            print(f"{Fore.BLUE}Author: {Fore.GREEN}{book[1]}")
            print(f"{Fore.BLUE}Path: {Fore.GREEN}{book[2]}")
            print(f"{Fore.BLUE}Folder: {Fore.GREEN}{book[3]}")
            print(f"{Fore.BLUE}Genre: {Fore.GREEN}{book[4]}")
            print("\n")

    @staticmethod
    def display(array):
        """
        Prints out the names of the ebooks passed in the array argument.
        """
        print("\n")
        x = 1
        for element in array:
            print(f"{Fore.GREEN}#{x} {element[0]}")
            x += 1
        print("\n")

    @staticmethod
    def do_clear(arg):
        """
        Clear the console.
        """
        try:
            os.system("cls")
        except OSError:
            os.system("clear")

    @staticmethod
    def do_quit(arg):
        """
        Exit the console.
        """
        quit()


if __name__ == "__main__":
    app = App()
    app.cmdloop()
