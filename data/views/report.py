from rest_framework.viewsets import ViewSet
from rest_framework.response import Response


class ReportViewClass(ViewSet):
    def get(self, request, customer_code, retail_store_code):
        return Response({"Report":f"Report of the retail store with code: {retail_store_code}"})

    def get_all(self, request, customer_code):
        return Response({"Report":"SUCCESSFULLY"})
