def test_pipeline(a='a',b='7'):
    add_task = add(a, b)
    substract_task = substract(add_task.output, b)