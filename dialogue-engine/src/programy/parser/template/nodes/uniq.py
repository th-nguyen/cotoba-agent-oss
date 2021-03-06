"""
Copyright (c) 2020 COTOBA DESIGN, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from programy.utils.logging.ylogger import YLogger

from programy.parser.template.nodes.get import TemplateGetNode
from programy.parser.template.nodes.triple import TemplateTripleNode
from programy.parser.exceptions import ParserException


class TemplateUniqNode(TemplateTripleNode):

    def __init__(self, subj=None, pred=None, obj=None):
        TemplateTripleNode.__init__(self, node_name="uniq", subj=subj, pred=pred, obj=obj)

    def resolve_to_string(self, client_context):
        rdf_subject = None
        rdf_predicate = None
        rdf_object = None

        if self._subj is not None:
            rdf_subject = self._subj.resolve(client_context).upper()
        if self._pred is not None:
            rdf_predicate = self._pred.resolve(client_context).upper()
        if self._obj is not None:
            rdf_object = self._obj.resolve(client_context)

        results = client_context.brain.rdf.match_only_vars(rdf_subject, rdf_predicate, rdf_object)

        values = []
        for result in results:
            for pair in result:
                if pair[1] not in values:
                    values.append(pair[1])

        resolved = ""
        if values:
            resolved = " ".join(values)
        else:
            resolved = TemplateGetNode.get_default_value(client_context)

        YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        return "[UNIQ]"

    def to_xml(self, client_context):
        xml = "<uniq>"
        xml += self.children_to_xml(client_context)
        xml += "</uniq>"
        return xml

    def parse_expression(self, graph, expression):
        super(TemplateUniqNode, self).parse_expression(graph, expression)

        if self._subj is None and self._pred is None and self._obj is None:
            raise ParserException("Subject/Predicate/Object element missing", xml_element=expression, nodename='uniq')
