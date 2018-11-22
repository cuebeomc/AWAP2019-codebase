package(default_visibility = ['//visibility:public'])

py_binary(
    name = 'game',
    main = 'game.py',
    srcs = ['game.py'],
    deps = [
        ':board',
        ':tile'
    ],
)

py_library(
    name = 'board',
    srcs = ['board.py'],
    deps = [
        ':tile'
    ],
)

py_library(
    name = 'tile',
    srcs = ['tile.py'],
)
