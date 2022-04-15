from django import template
from analyses.models import Analysis

register = template.Library()


@register.filter()
def map_status(status):
    if status == True:
        return 'dostupné'
    if status == False:
        return 'nedostupné'
    if status == Analysis.Status.PENDING:
        return 'v poradí'
    if status == Analysis.Status.IN_PROGRESS:
        return 'rozpracovaná'
    if status == Analysis.Status.FINISHED:
        return 'hotovo'
        
