class Document:
    def __str__(self):
        tag = self.get_tag()
        namespaces = ''
        if self.xml_namespaces is not None:
            for ns in self.xml_namespaces:
                namespaces += f' {ns}'

        return f'<{tag}{namespaces}>{self.get_value()}</{tag}>'

    def get_xml_file_content(self):
        full_file = f'<?xml version="1.0" encoding="UTF-8" standalone="no"?>{self}'
        return full_file