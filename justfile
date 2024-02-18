prog := "yank"
home := env_var("HOME")
extensions := home / ".password-store/.extensions"

install:
    install -v -d "{{extensions}}"
    install -v "{{prog}}.py" "{{extensions}}/{{prog}}.py"
    install -v "{{prog}}.bash" "{{extensions}}/{{prog}}.bash"

uninstall:
    rm -vrf \
      "{{extensions}}/{{prog}}.bash" \
      "{{extensions}}/{{prog}}.py"

test:
    pytest -s
