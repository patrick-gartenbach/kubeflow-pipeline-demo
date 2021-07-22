
def add(a: float, b: float) -> float:
    '''Calculates sum of two arguments'''
    return a + b

if __name__ == '__main__':
    import sys
    import kfp.components as comp    

    component_path = sys.argv[1]+sys.argv[2]

    comp.create_component_from_func(
    func=add,
    base_image='python:3.7', # Optional
    output_component_file= component_path)