from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .models import *

from rest_framework import status, viewsets
# Create your views here.
appUrl = '/todo'
todoURl = f'{appUrl}/'


def todoHome(request):
    try:
        todo = Todo.objects.filter(is_done=False)
        todoCompleted = Todo.objects.filter(is_done=True)
        # ---------------------------------------------------------
        #  home views count
        try:
            todo_count = Todo_page_view_count.objects.get(id=1)
            todo_count.todo_home_view_count += 1
            todo_count.save()
        except:
            pass
        # ---------------------------------------------------------
        try:
            if request.method == "POST":
                uid = request.POST["uid"]
                todo = Todo.objects.get(uid=uid)
                try:
                    if request.POST["done"] == "on":
                        done = True
                except:
                    done = False
                data = {"is_done": done}

                serializer = TodoSerializer(todo, data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                return redirect(todoURl)
        except:
            pass
    except:
        pass
    return render(request, "todohome.html", {'todo': todo, 'todoCompleted': todoCompleted})


def todoCreate(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        data = {"todo_title": title, "todo_description": description}

        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return redirect(todoURl)
        else:
            if len(title) < 3:
                messages.error(
                    request, "Title must be more than 2 characters.")
            if len(title) == 0:
                pass

    return render(request, 'todoCreate.html')


def todoUpdate(request, pk):
    todo = Todo.objects.get(uid=pk)
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        try:
            if request.POST["done"] == "on":
                done = True
            else:
                done = False
        except:
            done = False
        data = {"todo_title": title,
                "todo_description": description, "is_done": done}

        serializer = TodoSerializer(todo, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return redirect(todoURl)
        else:
            if len(title) < 3:
                messages.error(
                    request, "Title must be more than 2 characters.")
            if len(title) == 0:
                pass
    return render(request, 'todoUpdate.html', {'todo': todo})


def todoDelete(request, pk):
    tc = Todo.objects.all()
    if tc.count() > 5:
        todo = Todo.objects.get(uid=pk)
        todo.delete()
        return redirect(todoURl)
    else:
        return redirect(todoURl)


@api_view(['GET'])
def get_todo(request):
    todo_objs = Todo.objects.all()
    serializer = TodoSerializer(todo_objs, many=True)
    return Response({
        'status': True,
        "message": "Todo Fetched",
        'data': serializer.data,
    })


@api_view(['POST'])
def post_todo(request):
    try:
        data = request.data
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': True,
                "message": "Success Todo created",
                'data': serializer.data,
            })
        return Response({
            'status': False,
            "message": "Invalid Fields",
            'data': serializer.errors,
        })
    except Exception as e:
        return Response({
            'status': False,
            "message": f"{e}"
        })


@api_view(['PATCH'])
def patch_todo(request):
    try:
        data = request.data
        if not data.get('uid'):
            return Response({
                'status': False,
                "message": "uid is required",
                'data': {},
            })

        obj = Todo.objects.get(uid=data.get('uid'))
        serializer = TodoSerializer(obj, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': True,
                "message": "Success updated Todo",
                'data': serializer.data,
            })
        return Response({
            'status': False,
            "message": "Invalid data",
            'data': serializer.errors,
        })
    except Exception as e:
        return Response({
            'status': False,
            "message": f"{e}",
            'data': {},
        })


class TodoView(APIView):
    def get(self, request):
        todo_objs = Todo.objects.all()
        serializer = TodoSerializer(todo_objs, many=True)
        return Response({
            'status': True,
            "message": "Todo Fetched",
            'data': serializer.data,
        })

    def post(self, request):
        try:
            data = request.data
            serializer = TodoSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': True,
                    "message": "Success Todo created",
                    'data': serializer.data,
                })
            return Response({
                'status': False,
                "message": "Invalid Fields",
                'data': serializer.errors,
            })
        except Exception as e:
            return Response({
                'status': False,
                "message": f"{e}"
            })


class TodoViewSets(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
