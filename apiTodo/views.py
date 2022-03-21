from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view,action
from rest_framework.response import Response
from .models import Todo
from .serializers import TodoSerializer
from rest_framework import status

#* for CBV
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView,mixins,ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet

def home(request):
    return HttpResponse(
        '<center><h1 style="background-color:powderblue;">Welcome to ApiTodo</h1></center>'
    )
#*use decorators for rest_api
@api_view(['GET'])
def todoList(request):
    query = Todo.objects.all();
    #*using serializer
    serializer = TodoSerializer(query,many=True)
    return Response(serializer.data)


@api_view(['POST'])
def todoCreate(request):
    
    #*using serializer
    serializer = TodoSerializer(data =request.data)
    if serializer.is_valid():
        serializer.save()
    
    return Response(serializer.data)

#*get and post together
@api_view(['GET','POST'])
def todoListCreate(request):
    query = Todo.objects.all();
    
    if request.method == 'POST':
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save();
    elif request.method == 'GET':
        serializer = TodoSerializer(query,many=True)
        
    return Response(serializer.data)

#*single object
@api_view(['GET','PUT','DELETE'])
def todo_detail(request,pk):
        
    if request.method == 'GET':
        query = Todo.objects.all()
        serializer = TodoSerializer(query, many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        query = Todo.objects.get(id=pk)
        #*single res no many
        serializer = TodoSerializer(instance=query,data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)    
    elif request.method == 'DELETE':
        query= Todo.objects.get(id=pk)
        query.delete()
        return Response('Deleted',status= status.HTTP_204_NO_CONTENT)

# #*update view
# @api_view(['PUT'])
# def todo_update(request,pk):
    
#     query = Todo.objects.get(id=pk)
#     #*single res no many
#     serializer = TodoSerializer(instance=query,data=request.data)
#     if serializer.is_valid():
#         serializer.save()
        
#     return Response(serializer.data)

# #*get and put 
# @api_view(['GET','PUT','DELETE'])
# def todo_update(request,pk):
    
#     if request.method == 'GET':
#         query = Todo.objects.all()
#         serializer = TodoSerializer(query, many = True)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         query = Todo.objects.get(id=pk)
#         #*single res no many
#         serializer = TodoSerializer(instance=query,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data)    
#     elif request.method == 'DELETE':
#         query= Todo.objects.get(id=pk)
#         query.delete()
#         return Response('Deleted')

    
######## API VIEW ########

class TodoList(APIView) :
    
    #*if method==get
    def get(self, request):
        todos = Todo.objects.all()
        serializer =TodoSerializer(todos,many=True)
        return Response(serializer.data,status= status.HTTP_202_ACCEPTED)
    
    def post(self,request):
        serializer = TodoSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        #*if not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TodoDetail(APIView):
    
    def get_obj(self,pk):
        return get_object_or_404(Todo,id=pk)
    
    def get(self,request,pk):
        todo = self.get_obj(pk)
        serializer = TodoSerializer(todo)
        return Response(serializer.data)
    
    def put(self,request,pk):
        todo = self.get_obj(pk)
        serializer = TodoSerializer(instance=todo,data=request.data)
        if serializer.is_valid():
            serializer.save();
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        todo = self.get_obj(pk)
        todo.delete()
        data = {
            'message' : 'Succesfully deleted'
        }
        return Response(data = data,status=status.HTTP_204_NO_CONTENT)
        

########## Genericapi view #########################

class TodoListCreate(mixins.ListModelMixin,mixins.CreateModelMixin,GenericAPIView):
    #*from generalapiview to override
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    
    #* mixin & genericapiview
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    
    def post(self,request,*args,**kwargs):
        return self.create(request, *args, **kwargs)
    
####### Generics ##########

class TodoListCreateGen(ListCreateAPIView):
    #*from generalapiview to override
    #*no need to write
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    
    
class TodoGetUpdDelGen(RetrieveUpdateDestroyAPIView):
    #*from generalapiview to override
    #*no need to write
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    

######## Viewsets ##########
#write your view with sets and generics or user built-in classes
class TodoModelView(ModelViewSet):
    #*from generalapiview to override
    #*no need to write
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    
    #*custom path route
    @action(methods=["GET"],detail=False)
    def todo_count(self,request):
        todo_count = Todo.objects.filter(done=False).count()
        count={
            'counts':todo_count
        }
        
        return Response(count)