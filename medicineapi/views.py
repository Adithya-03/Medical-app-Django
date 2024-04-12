from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from medicine.forms import Medicinedata
from medicine.models import Medicine
from .serializer import ProductSerializer
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm



@api_view(['POST'])
@permission_classes((AllowAny,))
def signupapi(request):
    form = UserCreationForm(data=request.data)
    if form.is_valid():
        user = form.save()
        return Response("account created successfully", status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def loginapi(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def create_product(request):
    form = Medicinedata(request.POST)
    if form.is_valid():
        medicines = form.save()
        return Response({'id': medicines.id}, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes((AllowAny,))
def list_products(request):
    products = Medicine.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)



from django.shortcuts import get_object_or_404


@api_view(['PUT'])
@permission_classes((AllowAny,))
def update_product(request, pk):
    product = get_object_or_404(Medicine, pk=pk)
    form = Medicinedata(request.data, instance=product)
    if form.is_valid():
        form.save()
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    else:
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['DELETE'])
@permission_classes((AllowAny,))
def delete_product(request, pk):
    try:
        medicines= Medicine.objects.get(pk=pk)
    except medicines.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    medicines.delete()
    return Response("deleted successfully")


# @api_view(['GET'])
# @permission_classes((AllowAny,))
# def search_view(request):
#     if 'q' in request.GET:
#         q = request.GET['q']
#         # Construct a query to search for 'name' containing the search query
#         search_query = Q(name__exact=q)
#         # Filter Medicine objects based on the search query
#         medicine_list = Medicine.objects.filter(search_query)
#         serializer = ProductSerializer( medicine_list, many=True)
#         return Response(serializer.data)
#         # print(medicine_list)
#         # context = {
#         #     'medicine_list': medicine_list,
#         #     'query': q,
#         # }
#         # return render(request, 'search_results.html', context)
#     else:
#         # If no search query provided, return an empty search page or handle it accordingly
# #          return Response("no such data")




# @api_view(['GET'])
# @permission_classes((AllowAny,))
# def search_product(request):
#     if 'q' in request.GET:
#         q = request.GET['q']
#         print(q)
#         # Construct a query to search for 'name' containing the search query
#         search_query = Q(name__icontains=q)  # Using 'icontains' for case-insensitive search
#         # Filter Medicine objects based on the search query
#         medicine_list = Medicine.objects.filter(search_query)
#         serializer = ProductSerializer(medicine_list, many=True)
#         return Response(serializer.data)
#     else:
#         # If no search query provided, return an error response
#         return Response({"error": "No search query provided"}, status=400)


# from rest_framework import filters
# from rest_framework.generics import ListAPIView
# from rest_framework.filters  import SearchFilter

# # class QuestionsAPIView(generics.ListCreateAPIView):
# #     search_fields = ['name']
# #     filter_backends = (filters.SearchFilter,)
# #     queryset = Medicine.objects.all()
# #     serializer_class = ProductSerializer
# class QuestionsAPIView(ListAPIView):
#     queryset = Medicine.objects.all()
#     serializer_class = ProductSerializer
#     filter_backends = [SearchFilter]
#     search_fields = ['name']



# class SearchAPIView(APIView):
#     def get(self, request):
#         # Get the search query parameter 'q' from the request
#         q = request.query_params.get('q', None)
#         if q:
#             # Filter Medicine objects based on the search query
#             medicines = Medicine.objects.filter(name__icontains=q)
#             # Serialize the queryset
#             serializer = ProductSerializer(medicines, many=True)
#             return Response(serializer.data)
#         else:
#             # If no search query provided, return an empty response or handle it accordingly
#             return Response({"detail": "No search query provided."}, status=status.HTTP_400_BAD_REQUEST)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.filters import SearchFilter
from medicine.models import Medicine
from .serializer import ProductSerializer

class SearchAPIView(APIView):
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']
    authentication_classes = [] 
    permission_classes = [AllowAny]

    def get_queryset(self):
        q = self.request.query_params.get('q', None)
        if q:
            return Medicine.objects.filter(name__icontains=q)
        else:
            return Medicine.objects.none()

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


        
# from rest_framework.filters import SearchFilter
# from rest_framework.generics import ListAPIView
# class SearchAPIView(ListAPIView):
#     queryset = Medicine.objects.all()
#     serializer_class = ProductSerializer
#     filter_backends = [SearchFilter]
#     search_fields = ['name']
