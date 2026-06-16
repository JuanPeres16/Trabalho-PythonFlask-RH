from datetime import datetime
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


class PdfService:
    def employees_report(self, employees, generated_by):
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=landscape(A4),
            rightMargin=28,
            leftMargin=28,
            topMargin=58,
            bottomMargin=42,
        )
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph("Relatorio de Colaboradores", styles["Title"]))
        elements.append(
            Paragraph(
                f"Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')} por {generated_by}",
                styles["Normal"],
            )
        )
        elements.append(Spacer(1, 14))

        rows = [
            ["Nome", "E-mail", "Departamento", "Cargo", "Status", "Admissao"],
        ]
        for employee in employees:
            rows.append(
                [
                    employee.name,
                    employee.email,
                    employee.department.name if employee.department else "-",
                    employee.position.name if employee.position else "-",
                    employee.status,
                    employee.admission_date.strftime("%d/%m/%Y")
                    if employee.admission_date
                    else "-",
                ]
            )

        table = Table(rows, repeatRows=1, colWidths=[140, 190, 115, 130, 70, 80])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#263238")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 8),
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#B0BEC5")),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F4F7F8")]),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        elements.append(table)
        elements.append(Spacer(1, 14))

        total = len(employees)
        ativos = len([employee for employee in employees if employee.status == "ativo"])
        inativos = len([employee for employee in employees if employee.status == "inativo"])
        elements.append(
            Paragraph(
                f"Total de colaboradores: {total} | Ativos: {ativos} | Inativos: {inativos}",
                styles["Heading3"],
            )
        )

        doc.build(elements, onFirstPage=self._footer, onLaterPages=self._footer)
        buffer.seek(0)
        return buffer

    def _footer(self, canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.drawString(28, 22, "PeopleFlow - Sistema de Gestao de Colaboradores")
        canvas.drawRightString(doc.pagesize[0] - 28, 22, f"Pagina {doc.page}")
        canvas.restoreState()
