import tkinter as tk

from interface import TaskManagerApp


def main():
    try:
        app = TaskManagerApp()
        app.mainloop()
    except tk.TclError as exc:
        print(f"Não foi possível iniciar a interface: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
