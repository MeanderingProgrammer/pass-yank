lib := "/usr/local/lib"
extensions := lib / "password-store/extensions"

install:
    install -v -d "{{extensions}}"
    install -v "yank.py" "{{extensions}}/yank.py"
    install -v "yank.bash" "{{extensions}}/yank.bash"
