# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Dialog(Component):
    """A Dialog component.
SSB styled dialog component.
A wrapper for displaying a dialog

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    All rendered content.

- id (string; optional)

- className (string; optional):
    Optional container class."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'ssb_dash_components'
    _type = 'Dialog'
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, className=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'className']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'className']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(Dialog, self).__init__(children=children, **args)
