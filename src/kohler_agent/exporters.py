"""Turn a rendered answer into downloadable files in every requested format.

Each `_xxx_export` helper is independent and lazily imports its own heavy
dependency (python-docx, openpyxl, reportlab) so the rest of the app never
pays that import cost unless a user actually clicks that download button.
"""

from __future__ import annotations

import csv
import html
import json
import zipfile
from io import BytesIO, StringIO

from .formatting import extract_json

EXPORT_LABELS: dict[str, str] = {
    "pdf": "PDF",
    "xlsx": "Excel",
    "docx": "Word",
    "json": "JSON",
    "xml": "XML",
    "csv": "CSV",
    "html": "HTML",
    "md": "Markdown",
    "txt": "Text",
    "zip": "All formats (ZIP)",
}


def _csv_export(answer: str, sources: list[str]) -> bytes:
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=["answer", "sources", "grounded"])
    writer.writeheader()
    writer.writerow({"answer": answer, "sources": "; ".join(sources), "grounded": bool(sources)})
    return output.getvalue().encode("utf-8")


def _docx_export(answer: str, response_format: str, sources: list[str]) -> bytes:
    from docx import Document
    from docx.shared import Inches, Pt

    document = Document()
    section = document.sections[0]
    section.top_margin = section.bottom_margin = Inches(0.7)
    section.left_margin = section.right_margin = Inches(0.8)
    title = document.add_heading("KOHLER Unified Enterprise AI Agent", level=0)
    title.runs[0].font.size = Pt(20)
    document.add_paragraph(f"Response format: {response_format}")
    for line in answer.splitlines():
        stripped = line.strip()
        if not stripped:
            document.add_paragraph("")
        elif stripped.startswith("#"):
            document.add_heading(stripped.lstrip("#").strip(), level=min(stripped.count("#"), 3))
        elif stripped.startswith(("- ", "* ")):
            document.add_paragraph(stripped[2:], style="List Bullet")
        else:
            document.add_paragraph(stripped)
    document.add_heading("Sources", level=2)
    document.add_paragraph(", ".join(sources) if sources else "No source matched.")
    output = BytesIO()
    document.save(output)
    return output.getvalue()


def _xlsx_export(answer: str, response_format: str, sources: list[str]) -> bytes:
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Response"
    sheet["A1"] = "KOHLER Unified Enterprise AI Agent"
    sheet["A1"].font = Font(size=16, bold=True, color="FFFFFF")
    sheet["A1"].fill = PatternFill("solid", fgColor="1F4E78")
    sheet.merge_cells("A1:B1")
    sheet["A3"], sheet["B3"] = "Response format", response_format
    sheet["A5"], sheet["B5"] = "Answer", answer
    sheet["A7"], sheet["B7"] = "Sources", "; ".join(sources) or "No source matched."
    for cell in ("A3", "A5", "A7"):
        sheet[cell].font = Font(bold=True)
    for cell in ("B5", "B7"):
        sheet[cell].alignment = Alignment(wrap_text=True, vertical="top")
    sheet.column_dimensions["A"].width = 22
    sheet.column_dimensions["B"].width = 110
    sheet.row_dimensions[5].height = max(60, min(480, 18 * (answer.count("\n") + 3)))
    sources_sheet = workbook.create_sheet("Sources")
    sources_sheet.append(["Source file"])
    for source in sources:
        sources_sheet.append([source])
    sources_sheet["A1"].font = Font(bold=True, color="FFFFFF")
    sources_sheet["A1"].fill = PatternFill("solid", fgColor="1F4E78")
    sources_sheet.column_dimensions["A"].width = 60
    output = BytesIO()
    workbook.save(output)
    return output.getvalue()


def _pdf_export(answer: str, response_format: str, sources: list[str]) -> bytes:
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
    from xml.sax.saxutils import escape

    output = BytesIO()
    document = SimpleDocTemplate(
        output,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title="KOHLER Unified Enterprise AI Agent response",
    )
    styles = getSampleStyleSheet()
    body = ParagraphStyle(
        "KohlerBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        alignment=TA_LEFT,
        spaceAfter=6,
    )
    heading = ParagraphStyle(
        "KohlerHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        spaceBefore=8,
        spaceAfter=6,
    )
    story: list = [
        Paragraph("KOHLER Unified Enterprise AI Agent", styles["Title"]),
        Paragraph(f"Response format: {escape(response_format)}", body),
        Spacer(1, 6),
    ]
    for line in answer.splitlines():
        safe_line = escape(line).replace("  ", "&nbsp;&nbsp;")
        if line.strip().startswith("#"):
            story.append(Paragraph(escape(line.lstrip("#").strip()), heading))
        elif line.strip():
            story.append(Paragraph(safe_line, body))
        else:
            story.append(Spacer(1, 5))
    story.extend(
        [
            Spacer(1, 8),
            Paragraph("Sources", heading),
            Paragraph(escape(", ".join(sources) or "No source matched."), body),
        ]
    )
    document.build(story)
    return output.getvalue()


def export_response_files(
    answer: str, response_format: str, sources: list[str]
) -> dict[str, tuple[bytes, str, str]]:
    """Return {extension: (bytes, filename, mime_type)} for every supported
    export format, plus a "zip" entry bundling all of them together."""
    safe_answer = answer.strip() or "The local model returned an empty response."
    base = "kohler_agent_response"
    files: dict[str, tuple[bytes, str, str]] = {
        "txt": (safe_answer.encode(), f"{base}.txt", "text/plain"),
        "md": (safe_answer.encode(), f"{base}.md", "text/markdown"),
        "json": (
            json.dumps(
                extract_json(safe_answer) or {"answer": safe_answer, "sources": sources},
                indent=2,
                ensure_ascii=False,
            ).encode(),
            f"{base}.json",
            "application/json",
        ),
        "xml": (
            (
                "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<response>\n"
                f"  <answer>{html.escape(safe_answer)}</answer>\n"
                f"  <sources>{html.escape(', '.join(sources) or 'none')}</sources>\n"
                "</response>\n"
            ).encode(),
            f"{base}.xml",
            "application/xml",
        ),
        "csv": (_csv_export(safe_answer, sources), f"{base}.csv", "text/csv"),
        "html": (
            (
                "<!doctype html><html><head><meta charset=\"utf-8\">"
                "<title>KOHLER Agent Response</title><style>"
                "body{font-family:Arial;max-width:900px;margin:40px auto;line-height:1.6}"
                "pre{white-space:pre-wrap;background:#f4f6f8;padding:20px}"
                "</style></head><body><h1>KOHLER Unified Enterprise AI Agent</h1>"
                f"<p>Format: {html.escape(response_format)}</p>"
                f"<pre>{html.escape(safe_answer)}</pre>"
                f"<p><b>Sources:</b> {html.escape(', '.join(sources) or 'none')}</p>"
                "</body></html>"
            ).encode(),
            f"{base}.html",
            "text/html",
        ),
        "docx": (
            _docx_export(safe_answer, response_format, sources),
            f"{base}.docx",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ),
        "xlsx": (
            _xlsx_export(safe_answer, response_format, sources),
            f"{base}.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ),
        "pdf": (_pdf_export(safe_answer, response_format, sources), f"{base}.pdf", "application/pdf"),
    }
    archive_output = BytesIO()
    with zipfile.ZipFile(archive_output, "w", zipfile.ZIP_DEFLATED) as archive:
        for data, filename, _mime in files.values():
            archive.writestr(filename, data)
    files["zip"] = (archive_output.getvalue(), f"{base}_all_formats.zip", "application/zip")
    return files
