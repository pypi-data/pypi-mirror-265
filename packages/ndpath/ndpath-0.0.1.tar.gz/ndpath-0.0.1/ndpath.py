import os
import shlex
from rich import print
from rich.console import Console
import readchar


class Ndpath:
    def __init__(self):
        self.console = Console()
        self.paths = self.init_paths()
        self.selected_index = 0
        self.scroll_index = 0
        self.help = self.load_help_text()
        self.error = ""

    def run(self):
        while True:
            self.clear_screen()
            key = readchar.readkey()
            if key == "q":
                yes = input("Save your changes? (y/n): ").lower() == "y"
                if yes:
                    self.save_env_file()
                break
            elif key == readchar.key.UP:
                if self.selected_index > 0:
                    self.selected_index -= 1
                    if self.selected_index < self.scroll_index:
                        self.scroll_index = self.selected_index
            elif key == readchar.key.DOWN:
                if self.selected_index < len(self.paths) - 1:
                    self.selected_index += 1
                    terminal_height, _ = os.get_terminal_size()
                    if self.selected_index >= self.scroll_index + terminal_height - 5:
                        self.scroll_index = self.selected_index - terminal_height + 6
            elif key == readchar.key.PAGE_UP:
                terminal_height, _ = os.get_terminal_size()
                self.selected_index = max(0, self.selected_index - terminal_height + 5)
                self.scroll_index = max(0, self.scroll_index - terminal_height + 5)
            elif key == readchar.key.PAGE_DOWN:
                terminal_height, _ = os.get_terminal_size()
                self.selected_index = min(
                    len(self.paths) - 1, self.selected_index + terminal_height - 5
                )
                self.scroll_index = min(
                    len(self.paths) - terminal_height + 5, self.scroll_index + terminal_height - 5
                )
            else:
                self.handle_key_event(key)

    def paths_from_env(self):
        if os.path.exists(self.env_file()):
            return False
        return os.environ["PATH"].split(":")

    def env_file_contents(self):
        with open(self.env_file(), "r") as file:
            return file.read().replace("export PATH=", "").strip()

    def paths_from_env_file(self):
        return self.env_file_contents().split(":")

    def init_paths(self):
        return self.paths_from_env() or self.paths_from_env_file()

    def handle_key_event(self, key):
        if key == "o":
            self.insert_path(False)
        elif key == "O":
            self.insert_path(True)
        elif key == "x":
            self.remove_path()
        elif key == "X":
            self.remove_nonexistent_paths()
        elif key == "D":
            self.remove_duplicate_paths()
        elif key == "S":
            self.save_env_file()

    def env_file(self):
        return os.path.expanduser("~/.pathos.env")

    def quoted_paths(self):
        return [shlex.quote(path) for path in self.paths]

    def export_text(self):
        return "export PATH=" + ":".join(self.quoted_paths())

    def save_env_file(self):
        with open(self.env_file(), "w+") as file:
            file.write(self.export_text())

    def insert_path(self, above):
        path = input("Enter new path: ")
        if os.path.exists(path):
            index = self.selected_index if above else self.selected_index + 1
            self.paths.insert(index, path)
            self.selected_index = index
        else:
            self.error = f"pathos.py ERROR: {path} does not exist"

    def remove_path(self):
        if self.paths:
            del self.paths[self.selected_index]
            self.selected_index = min(self.selected_index, len(self.paths) - 1)

    def remove_nonexistent_paths(self):
        self.paths = [path for path in self.paths if os.path.exists(path)]

    def remove_duplicate_paths(self):
        self.paths = list(dict.fromkeys(self.paths))

    def display_title(self):
        print("\n\n pathos - CLI for editing a PATH env variable\n\n")

    def clear_screen(self):
        print("\033[2J\033[H", end="")
        self.display_title()
        self.display_paths_menu()

    def default_colors(self):
        return {"color": "white", "background": "on black", "style": ""}

    def display_error(self):
        if self.error:
            self.console.print(self.error, style="bold red")
            self.error = ""

    def display_paths_menu(self):
        terminal_height, _ = os.get_terminal_size()
        half_height = (terminal_height - 5) // 2

        if self.selected_index < self.scroll_index + half_height:
            self.scroll_index = max(0, self.selected_index - half_height)
        elif self.selected_index >= self.scroll_index + terminal_height - 5 - half_height:
            self.scroll_index = self.selected_index - terminal_height + 6 + half_height
        visible_paths = self.paths[self.scroll_index : self.scroll_index + terminal_height - 5]

        for index, path in enumerate(visible_paths, start=self.scroll_index):
            style = ""
            if not os.path.exists(path):
                style = "red strike"
            if self.paths.count(path) > 1:
                style = "cyan italic"
            if index == self.selected_index:
                style = "yellow bold"
            cursor = ">" if index == self.selected_index else " "
            self.console.print(f"{cursor} {index + 1}. {path}", style=style)

        if self.scroll_index > 0:
            self.console.print("↑", style="green")
        if self.scroll_index + terminal_height - 5 < len(self.paths):
            self.console.print("↓", style="green")

        print(self.help)
        self.display_error()

        # Move the cursor back to the selected path
        selected_index_on_screen = self.selected_index - self.scroll_index
        print(f"\033[{selected_index_on_screen + 1}A", end="")

    def load_help_text(self):
        return """
    Keyboard shortcuts:
    q - quit (will be prompted to save)
    k/↑ - move selection up
    j/↓ - move selection down
    o - insert path below selection
    O - insert path above selection
    x - delete selected path
    X - delete all non-existent paths
    D - dedupe list of paths
    S - manually save
    """

    def key_bindings(self, key):
        if key.lower() in ["q", "up", "k", "down", "j", "o", "x", "d", "s"]:
            return key.lower()
        return None


def main():
    Ndpath().run()


if __name__ == "__main__":
    main()
