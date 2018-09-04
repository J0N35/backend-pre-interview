from rest_framework_xml.parsers import XMLParser


class CustomizedXMLParser(XMLParser):
    def _xml_convert(self, element):
        """
                convert the xml `element` into the corresponding python object
                """
        list_item_tag = [
            "list_item",
            "element"
        ]
        children = list(element)

        if len(children) == 0:
            return self._type_convert(element.text)
        else:
            # if the fist child tag is list-item means
            # all children are list-item
            if children[0].tag in list_item_tag:
                data = []
                for child in children:
                    data.append(self._xml_convert(child))
            else:
                data = {}
                for child in children:
                    data[child.tag] = self._xml_convert(child)
        return data
