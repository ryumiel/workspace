;; Per-directory local variables for GNU Emacs 23 and later.

;; Syntax: ((MODE (VAR . VAL) ...) ...)
;; MODE is a symbol like `c-mode', or `nil' for all modes.
((c-mode
  (indent-tabs-mode . nil)
  (c-basic-offset . 4))
 (c++-mode
  (indent-tabs-mode . nil)
  (c-basic-offset . 4))
 (java-mode
  (indent-tabs-mode . nil)
  (c-basic-offset . 4))
 (change-log-mode
  (indent-tabs-mode . nil))
 (nil . ((projectile-project-compilation-cmd . "make -j8 all")
         (projectile-project-test-cmd . "CAIRO_TEST_TARGET=image CAIRO_TEST_TARGET_FORMAT=rgb test/cairo-test-suite clip-complex-shape-with-mixed-antialias")
         (projectile-project-compilation-dir . "./")
         (gud-gdb-command-name . "gdb -i=mi --init-command /home/yoon/webkit/bin/projects/cairo/gdbinit")))
)
