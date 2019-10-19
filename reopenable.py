import ast


class Reopenable(type):
    classes = {}

    def __new__(cls, name, bases, dict):
        base = cls.classes.get(name)
        if base is not None:
            bases += (base,)
        ret = super().__new__(cls, name, bases, dict)
        cls.classes[name] = ret
        return ret


def reopen(name, bases, dict):
    if name in Reopenable.classes:
        return Reopenable(name, bases, dict)
    return type(name, bases, dict)


class ClassWrapper(ast.NodeTransformer):
    def visit_ClassDef(self, node):
        node.keywords.append(ast.keyword(
            arg='metaclass',
            value=ast.Name(id='reopen', ctx=ast.Load()),
        ))
        return node


def load_ipython_extension(ipython):
    ipython.push({'Reopenable': Reopenable, 'reopen': reopen})
    ipython.ast_transformers.append(ClassWrapper())


def unload_ipython_extension(ipython):
    ipython.ast_transformers.clear()
