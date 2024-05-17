prog := "yank"
pass_root := env("PASSWORD_STORE_DIR", env("HOME") / ".password-store")
extensions := pass_root / ".extensions"

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
