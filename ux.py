from main import templates


def display_alert(html_template, request, message, alert_type="alert"):
    templates.TemplateResponse(
        html_template, {"request": request, alert_type: message})