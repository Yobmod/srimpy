pip install pytest-monkeytype
py.test --monkeytype-output=./monkeytype.sqlite3
monkeytype list-modules
monkeytype stub some.module
monkeytype apply some.module > some/module.mt.pyi