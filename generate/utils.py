def retrieve_output(output, part):
    nested = output

    for location in part:
        nested = nested[location]

    return nested

def update_output(output, part, value):
    nested = output

    for location in part[:-1]:
        nested = nested[location]
            
    nested[part[-1]] = value