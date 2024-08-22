import jinja2

jinja_env = jinja2.Environment(keep_trailing_newline=True)


# jinja2 filter format long descriptions from schema.org
def format_description(_input: str, max_width=70, space=4):
    lines: [[str]] = [[]]
    splitted_input: [str] = _input.replace("\\n", '\n').split()
    cursor, word_cursor = 0, 0
    # word wrap
    while word_cursor < len(splitted_input):
        if cursor > max_width:
            lines.append([])
            cursor = 0
        lines[-1].append(splitted_input[word_cursor])
        cursor += len(splitted_input[word_cursor])
        word_cursor += 1

    spacing = ' ' * space
    return ("\n" +  spacing + '/// ').join([" ".join(line) for line in lines])


jinja_env.filters["format_description"] = format_description
