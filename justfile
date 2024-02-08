prefix := "/usr/local"
lib := prefix / "lib"
extensions := lib / "password-store/extensions"
script := "yank.bash"

install:
    install -v -d "{{extensions}}"
    install -vm 0755 "src/{{script}}" "{{extensions}}/{{script}}"
