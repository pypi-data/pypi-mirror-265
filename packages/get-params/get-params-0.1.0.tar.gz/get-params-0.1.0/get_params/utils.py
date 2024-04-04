import inspect

def find_fn(lib, module=None):
    modules = getattr(lib, "__all__")
    mapping = dict(zip([x.lower() for x in modules], modules))

    if module in mapping:
        module = mapping[module]
    if not module or module not in modules:
        raise ValueError(f"{module} not found.")
    return getattr(lib, module)

def get_required(module):
    if inspect.isclass(module):
        module = module.__init__

    params = inspect.signature(module).parameters
    defaults = {p: params[p].default for p in params if p != "self"}
    
    _params = {
        "src": module.__qualname__,
        "required": [],
        "optional": []
    }
    for k, v in defaults.items():
        if v != inspect._empty:
            _params["optional"].append(k)
        else:
            _params["required"].append(k)
    return _params