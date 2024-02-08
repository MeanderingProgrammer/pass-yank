home := env_var("HOME")
extensions := home / ".password-store/.extensions"

install:
    install -v -d "{{extensions}}"
    install -v "yank.py" "{{extensions}}/yank.py"
    install -v "yank.bash" "{{extensions}}/yank.bash"

uninstall:
    rm -vrf \
      "{{extensions}}/yank.bash" \
      "{{extensions}}/yank.py"

test:
    pytest -s
