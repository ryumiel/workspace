;; Per-directory local variables for GNU Emacs 23 and later.

;; Syntax: ((MODE (VAR . VAL) ...) ...)
;; MODE is a symbol like `c-mode', or `nil' for all modes.
((c-mode
  (indent-tabs-mode . nil)
  (c-basic-offset . 4))
 (c++-mode . ((c-file-style . "WebKit")))
 (java-mode
  (indent-tabs-mode . nil)
  (c-basic-offset . 4))
 (change-log-mode
  (indent-tabs-mode . nil))
 (nil . ((projectile-project-compilation-cmd . "build-webkit --fast --debug")
         (projectile-project-run-cmd . "run-minibrowser --debug")
         (projectile-project-test-cmd . "run-minibrowser --debug --wrapper '/usr/bin/gdbserver localhost:8080' --test --url '--no-timeout --show-webview ")
         (projectile-project-compilation-dir . "./")
         ))
)
