from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json
from review.models import Movie_details
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def basic(request):
    return HttpResponse("Hello world")

def movie_info(request):
    movie=request.GET.get ("movie")
    date=request.GET.get ("date")
    return JsonResponse({"status":"success","result":{"movie_name":movie,"relese_date":date}},status=200)
@csrf_exempt
def movies(request):
    if request.method=="POST":
        data=json.loads(request.body)
        rating_raw = data.get("rating",0 )
        rating_value = int(float(rating_raw))      
        rating_stars = "*" * rating_value
        movie=Movie_details.objects.create ( movie_name=data.get("movie_name"),relese_date=data.get("relese_date"),budget=data.get("budget"),rating=rating_value)
        return JsonResponse({"status":"success","message":"movie record unsted successfully","data":{
                "movie_name": data.get("movie_name"),
                "relese_date": data.get("relese_date"),
                "budget": data.get("budget"),
                # "rating": rating_value,
                "rating_stars": rating_stars}},status=200)
    # return JsonResponse({"error":"error occured"},status=400)


#  GET ----------------


    if request.method == "GET":

    # always read movie_name first
        movie_name = request.GET.get("movie_name")

    # case 1 → user passed movie_name
        if movie_name:
            try:
                movie = Movie_details.objects.get(movie_name=movie_name)
                rating_stars = "*" * movie.rating
                return JsonResponse({
                    "status": "success",
                    "data": {
                    "movie_name": movie.movie_name,
                    "relese_date": str(movie.relese_date),
                    "budget": movie.budget,
                    "rating_stars": rating_stars
                }
            }, status=200)

            except Movie_details.DoesNotExist:
                return JsonResponse(
                    {"status": "error", "message": "movie not found"},status=404
            )
        
    # case 2 → no movie_name → return all movies
    # all_movies = list(Movie_details.objects.all().values())
    # return JsonResponse({"status": "success", "data": all_movies}, status=200)

    if request.method == "PUT":
        data = json.loads(request.body)
        movie_name = data.get("movie_name")
        if not movie_name:
            return JsonResponse({"status": "error", "message": "movie_name required"}, status=400)

        try:
            movie = Movie_details.objects.get(movie_name=movie_name)
        except Movie_details.DoesNotExist:
            return JsonResponse({"status": "error", "message": "movie not found"}, status=404)

        # update safely
        if "relese_date" in data:
            movie.relese_date = data.get("relese_date")
        if "budget" in data:
            movie.budget = data.get("budget")
        if "rating" in data:
            try:
                movie.rating = int(float(data.get("rating")))
            except (ValueError, TypeError):
                pass
        movie.save()

        return JsonResponse({
            "status": "success",
            "message": "movie updated successfully",
            "data": {
                "movie_name": movie.movie_name,
                "relese_date": str(movie.relese_date),
                "budget": movie.budget,
                "rating_stars": "*" * (movie.rating or 0)
            }
        }, status=200)
    

    # DELETE ------

    if request.method == "DELETE":
        data = json.loads(request.body)
        movie_name = data.get("movie_name")
        if not movie_name:
            return JsonResponse({"status": "error", "message": "movie_name required"}, status=400)

        try:
            movie = Movie_details.objects.get(movie_name=movie_name)
            movie.delete()
            return JsonResponse({"status": "success", "message": "movie deleted successfully"}, status=200)
        except Movie_details.DoesNotExist:
            return JsonResponse({"status": "error", "message": "movie not found"}, status=404)

    # ---------------- Other ----------------
    return JsonResponse({"error": "invalid request"}, status=400)
