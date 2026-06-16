import traceback
from datetime import datetime, time

from flask import has_request_context, request, session

from app.extensions import mongo


class LogService:
    def save_log(
        self,
        acao,
        tipo_evento,
        tabela=None,
        registro_id=None,
        detalhes=None,
        usuario=None,
    ):
        payload = {
            "timestamp": datetime.utcnow(),
            "usuario": usuario or self._current_user(),
            "acao": acao,
            "tipo_evento": tipo_evento,
            "tabela": tabela,
            "registro_id": str(registro_id) if registro_id is not None else None,
            "detalhes": detalhes or {},
            "ip": self._ip(),
            "user_agent": self._user_agent(),
        }
        self._insert(payload)
        return payload

    def save_access_log(self, response, elapsed_ms):
        payload = {
            "timestamp": datetime.utcnow(),
            "usuario": self._current_user(),
            "acao": "ACCESS",
            "tipo_evento": "acesso_rota",
            "endpoint": request.path if has_request_context() else None,
            "metodo": request.method if has_request_context() else None,
            "status_code": response.status_code,
            "tempo_resposta": elapsed_ms,
            "ip": self._ip(),
            "user_agent": self._user_agent(),
            "detalhes": {"endpoint_name": request.endpoint if has_request_context() else None},
        }
        self._insert(payload)

    def save_error(self, error):
        payload = {
            "timestamp": datetime.utcnow(),
            "usuario": self._current_user(),
            "acao": "ERROR",
            "tipo_evento": "erro",
            "erro": str(error),
            "stack_trace": traceback.format_exc(),
            "endpoint": request.path if has_request_context() else None,
            "metodo": request.method if has_request_context() else None,
            "ip": self._ip(),
            "user_agent": self._user_agent(),
        }
        self._insert(payload)
        return payload

    def query_logs(self, filters=None, limit=100):
        filters = filters or {}
        query = {}

        usuario = (filters.get("usuario") or "").strip()
        acao = (filters.get("acao") or "").strip()
        data_inicial = filters.get("data_inicial")
        data_final = filters.get("data_final")

        if usuario:
            query["usuario"] = {"$regex": usuario, "$options": "i"}
        if acao:
            query["acao"] = {"$regex": acao, "$options": "i"}

        date_range = {}
        start = self._parse_date(data_inicial)
        end = self._parse_date(data_final, end_of_day=True)
        if start:
            date_range["$gte"] = start
        if end:
            date_range["$lte"] = end
        if date_range:
            query["timestamp"] = date_range

        try:
            return list(
                mongo.db.logs.find(query).sort("timestamp", -1).limit(int(limit or 100))
            )
        except Exception:
            return []

    def _insert(self, payload):
        try:
            mongo.db.logs.insert_one(payload)
        except Exception:
            pass

    def _current_user(self):
        if has_request_context():
            return session.get("user_email") or session.get("user_name") or "anonimo"
        return "sistema"

    def _ip(self):
        return request.headers.get("X-Forwarded-For", request.remote_addr) if has_request_context() else None

    def _user_agent(self):
        return request.headers.get("User-Agent") if has_request_context() else None

    def _parse_date(self, value, end_of_day=False):
        if not value:
            return None
        try:
            parsed = datetime.fromisoformat(value)
            if len(value) == 10 and end_of_day:
                parsed = datetime.combine(parsed.date(), time.max)
            return parsed
        except ValueError:
            return None
