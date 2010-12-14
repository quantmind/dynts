import dynts

from sphinx.util.compat import Directive
from docutils import nodes, statemachine


class dyntslist(nodes.General, nodes.Element):
    pass


class DynTsList(Directive):
    has_content = False
    required_arguments = 0

    def run(self):
        env = self.state.document.settings.env
        rawdocs = dynts.functions_docs()
        targetid = "dyntslist"
    
        source = self.state_machine.input_lines.source(
            self.lineno - self.state_machine.input_offset - 1)

        encoding = self.options.get(
            'encoding', self.state.document.settings.input_encoding)
        tab_width = self.options.get(
            'tab-width', self.state.document.settings.tab_width)
    

        if 'literal' in self.options:
            # Convert tabs to spaces, if `tab_width` is positive.
            if tab_width >= 0:
                text = rawtext.expandtabs(tab_width)
            else:
                text = rawtext
            literal_block = nodes.literal_block(rawtext, text, source=path)
            literal_block.line = 1
            return [literal_block]
        else:
            include_lines = statemachine.string2lines(
                rawdocs, tab_width, convert_whitespace=1)
            self.state_machine.insert_input(include_lines, 'dyntslist')
            return []



def setup(app):
    app.add_directive('dyntslist', DynTsList)

    
