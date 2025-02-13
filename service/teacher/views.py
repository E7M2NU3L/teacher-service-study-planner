from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@api_view(['POST'])
def Create_RAG(request):
    return Response({
        'message' : "RAG instance has been created successfully"
    })

@api_view(['POST'])
def AskQuestion(request):
    return Response({
        'answer' : "Response from the Google Gemini"
    })