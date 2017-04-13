;;; Directory Local Variables
;;; For more information see (info "(emacs) Directory Variables")

((c-mode . ((indent-tabs-mode . t)
            (c-basic-offset . 4)))
 (nil . ((projectile-project-compilation-cmd . "make -j8 all")
         (projectile-project-test-cmd . "CAIRO_TEST_TARGET=image CAIRO_TEST_TARGET_FORMAT=rgb test/cairo-test-suite clip-complex-shape-with-mixed-antialias")
         (projectile-project-compilation-dir . "./")
         (gud-gdb-command-name . "gdb -i=mi --init-command /home/yoon/webkit/bin/projects/cairo/gdbinit")))
)
