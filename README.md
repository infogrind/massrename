# massrename

## Syntax:

    massrename [options] <directory> <pattern> <replacement>

Massrename renames all files in `<directory>` that match the regular expression
`<pattern>` using the substitution string `<replacement>`. The substitution string
can contain `\1`, `\2`, … if there are corresponding groups in the pattern.

## Options:

    Options:
    -h  Show this help text.
    -v  Display verbose output.
    -i  Ignore case in regular expression.
    -r  Recursive mode.
    -f  Force mode: does not ask for confirmation before renaming.
    -r  Recursive mode
