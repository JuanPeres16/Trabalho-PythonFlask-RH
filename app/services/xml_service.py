from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, tostring


class XmlService:
    def logs_to_xml(self, logs):
        root = Element("logs")

        for index, log in enumerate(logs, start=1):
            evento = SubElement(root, "evento", id=str(index))
            SubElement(evento, "usuario").text = str(log.get("usuario") or "")
            SubElement(evento, "acao").text = str(log.get("acao") or "")
            SubElement(evento, "descricao").text = self._descricao(log)
            SubElement(evento, "data_hora").text = self._date(log.get("timestamp"))
            SubElement(evento, "tipo_evento").text = str(log.get("tipo_evento") or "")
            SubElement(evento, "ip_origem").text = str(log.get("ip") or "")

            dados = SubElement(evento, "dados_vinculados")
            SubElement(dados, "tabela").text = str(log.get("tabela") or "")
            SubElement(dados, "registro_id").text = str(log.get("registro_id") or "")

        rough = tostring(root, encoding="utf-8")
        pretty = minidom.parseString(rough).toprettyxml(indent="  ", encoding="UTF-8")
        return pretty

    def _date(self, value):
        return value.isoformat() if hasattr(value, "isoformat") else str(value or "")

    def _descricao(self, log):
        if log.get("erro"):
            return str(log.get("erro"))
        detalhes = log.get("detalhes") or {}
        if isinstance(detalhes, dict) and detalhes.get("endpoint_name"):
            return f"Acesso a {log.get('endpoint')}"
        return str(detalhes) if detalhes else str(log.get("endpoint") or "")
