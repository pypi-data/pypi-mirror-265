import curses
import locale


class TerminalUI:
    def __init__(self):
        self.stdscr = curses.initscr()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        locale.setlocale(locale.LC_ALL, "")  # Padrão UTF-8

    def type_message(
        self, message, type_vel=30, delay_before=0, color=1, wrap_line=True
    ):
        if delay_before > 0:
            curses.napms(delay_before)

        for char in message:
            # Verifica se o cursor está na última linha da tela antes de adicionar um novo caractere
            if curses.getsyx()[0] == curses.LINES - 1:
                self.stdscr.scroll(
                    1
                )  # Rolagem para cima para liberar espaço para o novo caractere
            self.stdscr.addch(char, curses.color_pair(color))
            self.stdscr.refresh()
            curses.napms(type_vel)

        if wrap_line:
            # Verifica se o cursor está na última linha da tela antes de adicionar uma nova linha
            if curses.getsyx()[0] == curses.LINES - 1:
                self.stdscr.scroll(
                    1
                )  # Rolagem para cima para liberar espaço para a nova linha
            self.stdscr.addch("\n")

    def render_menu(self, menu_items):
        while True:
            for i, item in enumerate(menu_items):
                self.type_message(f"{i+1}. ", wrap_line=False, color=3, type_vel=5)
                self.type_message(item, color=1)

            self.type_message(
                "Escolha um número: ", wrap_line=False, color=2, type_vel=5
            )

            try:
                user_choice = int(self.stdscr.getstr().decode())
                if 1 <= user_choice <= len(menu_items):
                    return menu_items[user_choice - 1]
                else:
                    self.type_message("Opção inválida. Tente novamente.", color=4)
            except ValueError:
                self.type_message("Entrada inválida. Digite um número válido.", color=4)
            except curses.error:
                pass

    def run_forever(self):
        while True:
            try:
                self.stdscr.refresh()
            except KeyboardInterrupt:
                self.close()
                break

    def close(self):
        curses.endwin()


if __name__ == "__main__":
    ui = TerminalUI()
    ui.type_message("Hello world!")
    lost = ["Kaic", "Salomao"]
    selected = ui.render_menu(lost)
    ui.type_message(selected)
