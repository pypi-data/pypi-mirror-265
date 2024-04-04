# `get-params`
this package allows you to fetch the arguments of a function from a simple search string, matching a function within a module.

## usage
```python
import pandas
loss_fn = find_fn(lib=pandas, module="dataframe")
get_required(loss_fn)
```

Output:
```python
{'src': 'DataFrame.__init__',
  'required': [],
  'optional': ['data', 'index', 'columns', 'dtype', 'copy']}
```

## installation

you can install the package using pip:

```bash
pip install get-params
```

or locally:

```bash
git clone <repo>
cd <repo>
pip install .
```

the package can be useful when you want to be flexible with arguments passed to e.g. a user interface, where you want to call a specific function.
it was developed to handle the many loss functions inside the [`sentence_transformers.losses`](https://github.com/UKPLab/sentence-transformers/blob/master/sentence_transformers/losses/__init__.py).