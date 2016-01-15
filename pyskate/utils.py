def compare_proposed_to_running(proposed_config, running_config):
    '''Return diff between *proposed_config* and *running_config*.'''

    # remove empty lines from playbook
    for line in proposed_config:
        if len(line) == 0:
            proposed_config.remove(line)

    final_config = proposed_config[:]


    # all commands starting with "no "
    no_commands = [line.strip() for line in final_config if line.startswith('no ')]
    # all other commands
    commands = [line.strip() for line in final_config if not line.startswith('no ')]

    # commands starting with "no " that have a matching line in running_config
    # which means that it shall be included in the final_config committed to
    # device. all other "no " commands shall be disregarded when committing
    # the configuration.
    no_commands_real = []

    for line in running_config:
        for no_line in no_commands:
            if line == no_line.lstrip('no '):
                no_commands_real.append(no_line)
        if line in commands:
            commands.remove(line)

    return commands + no_commands_real
