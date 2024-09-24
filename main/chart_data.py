from django.db.models import Count

def chart_data(visit_queryset):
    diagnize_data = visit_queryset.values('diagnize_classification').annotate(count=Count('diagnize_classification'))
    status_data = visit_queryset.values('status').annotate(count=Count('status'))
    
    # Prepare the data for the charts
    diagnize_classification = {
        'labels': [item['diagnize_classification'] for item in diagnize_data],
        'counts': [item['count'] for item in diagnize_data],
    }
    
    status = {
        'labels': [item['status'] for item in status_data],
        'counts': [item['count'] for item in status_data],
    }
    return diagnize_classification, status