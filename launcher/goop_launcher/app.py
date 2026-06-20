"""The front-facing GTK3 launcher window for the Winlator-style Goop mod.

The UI is deliberately small: diagnose, prepare a prefix, and launch Roblox.
The implementation still uses the original Wine/DXVK/Roblox workflow, but the
labels and layout now reflect a more Winlator-like container experience.
"""

from __future__ import annotations

import sys
import threading

from . import __version__
from . import checks, config, roblox, wine


def _import_gtk():
    """Import gi lazily so unit tests never need a display."""
    import gi  # type: ignore[import-not-found]
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk  # type: ignore[import-not-found]
    return Gtk


class GoopWindow:
    def __init__(self, Gtk) -> None:
        self.Gtk = Gtk
        win = Gtk.Window(title=f"{config.APP_NAME} {__version__}")
        win.set_default_size(560, 420)
        win.connect("destroy", Gtk.main_quit)

        outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        outer.set_margin_top(12)
        outer.set_margin_bottom(12)
        outer.set_margin_start(12)
        outer.set_margin_end(12)
        win.add(outer)

        title = Gtk.Label(label=(
            f"<b>{config.APP_NAME}</b>\n"
            f"Winlator-style container workflow for Roblox\n"
            f"Wine {config.WINE_VERSION} + DXVK {config.DXVK_VERSION}"
        ))
        title.set_use_markup(True)
        title.set_line_wrap(True)
        outer.pack_start(title, False, False, 0)

        btns = Gtk.Box(spacing=8)
        outer.pack_start(btns, False, False, 0)

        self.btn_diag = Gtk.Button(label="Diagnose")
        self.btn_install = Gtk.Button(label="Prepare Prefix")
        self.btn_play = Gtk.Button(label="Launch Roblox")
        for b in (self.btn_diag, self.btn_install, self.btn_play):
            btns.pack_start(b, True, True, 0)

        self.btn_diag.connect("clicked", self._on_diagnose)
        self.btn_install.connect("clicked", self._on_install)
        self.btn_play.connect("clicked", self._on_play)

        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(True)
        outer.pack_start(scroll, True, True, 0)

        self.buf = Gtk.TextBuffer()
        view = Gtk.TextView(buffer=self.buf)
        view.set_editable(False)
        view.set_monospace(True)
        scroll.add(view)

        self.win = win
        self._set_busy(False)

    def _set_busy(self, busy: bool) -> None:
        for b in (self.btn_diag, self.btn_install, self.btn_play):
            b.set_sensitive(not busy)

    def _log(self, text: str) -> None:
        self.buf.insert(self.buf.get_end_iter(), text + "\n")

    def _on_diagnose(self, _btn) -> None:
        self._log("Running diagnostics…")
        self._set_busy(True)

        def work() -> None:
            diag = checks.run_all()
            self.Gtk.idle_add(self._finish_diagnose, diag)

        threading.Thread(target=work, daemon=True).start()

    def _finish_diagnose(self, diag) -> bool:
        self._log(diag.summary())
        if diag.launchable:
            self._log("✓ System is ready. Press Launch Roblox.")
        else:
            self._log("✗ Fix the blockers above before launching.")
        self._set_busy(False)
        return False

    def _on_install(self, _btn) -> None:
        self._log("Preparing a Winlator-style prefix…")
        self._set_busy(True)

        def work() -> None:
            try:
                exe = roblox.download_launcher()
                wine.init_prefix()
                if not wine.verify_prefix():
                    self.Gtk.idle_add(
                        self._fail,
                        "The prefix is missing DXVK DLLs. Re-run the setup flow.",
                    )
                    return
                staged = roblox.stage(exe)
                self.Gtk.idle_add(self._ok_install, staged)
            except Exception as exc:  # noqa: BLE001
                self.Gtk.idle_add(self._fail, str(exc))

        threading.Thread(target=work, daemon=True).start()

    def _ok_install(self, staged) -> bool:
        self._log(f"Staged {staged.name}. Ready to play.")
        self._set_busy(False)
        return False

    def _fail(self, msg: str) -> bool:
        self._log(f"✗ {msg}")
        self._set_busy(False)
        return False

    def _on_play(self, _btn) -> None:
        self._log("Launching Roblox under the Winlator-style prefix…")
        self._set_busy(True)

        def work() -> None:
            try:
                rc = roblox.launch()
                self.Gtk.idle_add(self._finish_play, rc)
            except Exception as exc:  # noqa: BLE001
                self.Gtk.idle_add(self._fail, str(exc))

        threading.Thread(target=work, daemon=True).start()

    def _finish_play(self, rc: int) -> bool:
        self._log(f"Roblox exited with code {rc}.")
        self._set_busy(False)
        return False

    def show(self) -> None:
        self.win.show_all()


def main() -> int:
    try:
        Gtk = _import_gtk()
    except (ImportError, ValueError) as exc:
        sys.stderr.write(
            f"winlator-goop: cannot start GUI: {exc}\n"
            "Install `python3-gi` and `gir1.2-gtk-3.0` (apt), then retry.\n"
        )
        return 2
    win = GoopWindow(Gtk)
    win.show()
    Gtk.main()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
