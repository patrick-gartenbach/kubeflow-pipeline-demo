
def add(a: float, b: float) -> float:
    '''Calculates sum of two arguments'''
    return a + b

if __name__ == '__main__':
    import sys
    import kfp.components as comp    

    comp.create_component_from_func(
    func=add,
    base_image='python:3.7', # Optional
    output_component_file= sys.argv[1])
