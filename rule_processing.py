

rules = {}
rule_path = 'data/Old_rule/rule_comprehensive.md'
new_rule_path ='data/Rules/new_rule_comprehensive.md'

def read_rule_file():
    with open(rule_path, 'r', encoding="utf-8-sig") as rule_file:
        rule_lines = rule_file.readlines()

    for line in rule_lines:
        line = line.strip()
        line_split = line.split(".", 1)
        if len(line_split) == 2:
            rules[line_split[0]] = line_split[1]

def concat_rules():
    new_rule_lines = ''
    for rule_id, rule_text in rules.items():
        ids = rule_id.split('-')
        if len(ids) > 1:
            newRule = ''
            not_first = False
            last_id = ''
            for id in ids:
                if(not_first):
                    id = f'{last_id}-{id}'

                newRule += f'{id}. {rules[id]}; '
                not_first = True
                last_id = id
            new_rule_lines += f'{newRule}\n'
        else:
            newRule = f'{ids[0]}. {rules[ids[0]]}\n'
            new_rule_lines += newRule
    return new_rule_lines

def write_new_rule_file(new_lines):
    with open(new_rule_path, 'w', encoding="utf-8-sig") as rule_file:
        rule_file.write(new_lines)

if __name__ == '__main__':
    read_rule_file()
    new_lines = concat_rules()
    write_new_rule_file(new_lines)
