from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import Article
from .serializers import ArticleSerializer
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .scraping import crunchscrape, venturescrape, vergescrape
import datetime

class DailyArticleAPIView(APIView):
    def get(self, request, *args, **kwargs):
        today = datetime.now().date()
        data = Article.objects.filter(created_at__date=today).order_by('-created_at')
    
        serializer = ArticleSerializer(data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class ScraperAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            results = {
                "crunchscrape": crunchscrape(),
                "venturescrape": venturescrape(),
                "vergescrape": vergescrape(),
            }
            return Response(results, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)