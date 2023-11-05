from .models import *
from dotenv import load_dotenv 
load_dotenv()
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import string
from .firebase import firebase_admin
from firebase_admin import auth
import random

class HelperFunctions:
# This function gets a unique username if the username already exists.
    def get_unique_username(username):
        '''
        This function first checks if provided username(given by user) exists in database or not. If id does not exist, 
        it returns the same username. If it exists, it appends a random string to the username and checks again. 
        It repeats this process until it finds a unique username.

        Parameters:
            username: string
        Returns:
            username: string
            exists: boolean
        '''

        # List of default usernames
        default_usernames = [
            "LuckyBreeze",
            "CyberNinja",
            "StarGazer24",
            "CoffeeAddict42",
            "MoonWalker99",
            "OceanExplorer",
            "TechGuru007",
            "NatureLover88",
            "QuantumCoder",
            "MusicMaestro23",
            "AdventureSeeker",
            "FitnessFanatic",
            "GameWizard56",
            "ArtisticSoul77",
            "ScienceGeek123",
            "TravelerWander",
            "BookWorm101",
            "FoodieDelight",
            "SkyDiverXtreme",
            "DreamChaser69"
        ]

        # Check if username is empty then give ine of default username
        if username == "":
            username = random.choice(default_usernames)

        if User.objects.filter(username=username).exists():
            # Infiinite loop to get a unique username
            while True:
                random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                username = username + "_"+random_str
                if not User.objects.filter(username=username).exists():
                    # infinite loop breaks when a unique username is found
                    return username, True
        return username, False

    # This function verifies the custom token from firebase
    def custom_token_verification(id_token):
        try:
            # decoding token using firebase_admin module
            decoded_token = auth.verify_id_token(id_token)
            return decoded_token
        except Exception as e:
            return None
  

class LoginSignupViews:
    @api_view(['POST'])
    def signup(request):
        '''
        This function creates a new user if the email and password are provided. It also checks if the username is unique or not.
        If the username is not unique, it appends a random string to the username and checks again. It repeats this process until it finds a unique username.

        Parameters:
            request: request object

        Returns:
            Response: response object
        '''

        try:
            # Check if email and password are provided
            if "email" not in request.data or "password" not in request.data:
                return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Getting all data from request
            data = request.data
            email = data['email']
            password = data['password']
            if 'first_name' in data:
                first_name = data['first_name']
            else:
                first_name = ''
            if 'last_name' in data:
                last_name = data['last_name']
            else:
                last_name = ''
            if 'username' in data:
                username = data['username']
            else:
                username = first_name + " " + last_name

            # Checking if password length is valid
            if len(password) < 8:
                return Response({'error': 'This password is too short. It must contain at least 8 characters'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Checking length of all fields is less than 100 
            if len(first_name) > 100 or len(email) > 100 or len(last_name) > 100 or len(password) > 100:
                return Response({'error': 'Only 100 characters are allowed for a field'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Getting unique username
            username, exists = HelperFunctions.get_unique_username(username)

            # Return error if username already exists along with possible usernames
            if exists:
                return Response({'error': 'A user with that username already exists. Available User name:' + str(username)}, status=status.HTTP_400_BAD_REQUEST)
            
            # Checking if email already exists
            if User.objects.filter(email=email).exists():
                return Response({'error': 'A user with that email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

            # Creating a user object
            user = User.objects.create(email=email, password=password, username=username, first_name=first_name, last_name=last_name)
            user.save()

            # Serializing user object
            user = UserSerializer(user).data

            # Returning response
            return Response({'message': 'User created successfully!','user' : user}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            # Returning error response - if some error occurs
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @api_view(['POST', 'GET'])
    def login(request):
        '''
        This function logs in a user if the email and password are provided.

        Parameters:
            request: request object

        Returns:
            Response: response object
        '''
        try:
            # Check if username and password are provided
            if "username" not in request.data or "password" not in request.data:
                return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Getting all data from request
            data = request.data
            username = data['username']
            password = data['password']

            # Checking if user exists
            if not User.objects.filter(username=username,password=password).exists():
                return Response({'error': 'Username or password is invalid'}, status=status.HTTP_400_BAD_REQUEST)
            
            # User exists so retrieving them
            user = User.objects.get(username=username, password=password)

            # Serializing user
            user_serialized = UserSerializer(user).data

            # Creating custom token for user using Firebase
            custom_token = auth.create_custom_token(uid=str(user.id))        
            
            # Generating full name and adding to return data
            full_name = user.first_name + "-" + user.last_name    
            user_serialized['full_name'] = full_name
            user_serialized['custom_token'] = custom_token

            # Returning response
            return Response({'message': 'User logged in successfully!', 'user': user_serialized}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ProfileViews:
    @api_view(['GET'])
    def get_profile(request):
        '''
        This function gets the profile of a user if the username is provided.

        Parameters:
            request: request object

        Returns:
            Response: response object   
        '''
        try:
            # Check if username is provided
            if "username" not in request.GET:
                return Response({'error': 'Username is required.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # verify custom token from firebase return 401 error if unauthorized 
            id_token = request.META.get('HTTP_AUTHORIZATION', '')
            decoded_token = HelperFunctions.custom_token_verification(id_token)
            if decoded_token is None:
                return Response({'detail': 'Invalid custom_token'}, status=status.HTTP_401_UNAUTHORIZED)


            # Getting all data from request
            username = request.GET['username']

            # Checking if user exists
            if not User.objects.filter(username=username).exists():
                return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Getting user object
            user = User.objects.get(username=username)

            # Serializing user object
            user_serialized = UserSerializer(user).data

            # Creating fullname
            full_name = user.first_name + "-" + user.last_name    
            user_serialized['full_name'] = full_name

            # Returning response
            return Response({'message': 'User profile fetched successfully!', 'user': user_serialized}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @api_view(['POST'])
    def edit_profile(request):
        '''
        This function edits the profile of a user if the username is provided.

        Parameters:
            request: request object

        Returns:
            Response: response object   
        '''
        try:
            # Check if username is provided
            if "username" not in request.data:
                return Response({'error': 'Usernameis required.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Getting all data from request
            data = request.data
            username = data['username']

            # Firebase check using custom token
            id_token = request.META.get('HTTP_AUTHORIZATION', '')
            decoded_token = HelperFunctions.custom_token_verification(id_token)
            if decoded_token is None:
                return Response({'detail': 'Invalid custom_token'}, status=status.HTTP_401_UNAUTHORIZED)
            
            # Checking if user exists
            if not User.objects.filter(username=username).exists():
                return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.get(username=username)

            if 'first_name' in data:
                user.first_name = data['first_name']
            if 'last_name' in data:
                    user.last_name = data['last_name']
            if "new_username" in data:
                new_username = data['new_username']
                new_username_unique, exists = HelperFunctions.get_unique_username(new_username)
                if exists:
                    return Response({'error': 'User already exist with the username ' + str(new_username)+ ". Please try : " + str(new_username_unique)}, status=status.HTTP_400_BAD_REQUEST)
                user.username = new_username_unique
            user.save()

            # Serializing user object
            user_serialized = UserSerializer(user).data

            # Creating fullname
            full_name = user.first_name + "-" + user.last_name    
            user_serialized['full_name'] = full_name

            # Returning response
            return Response({'message': 'User profile edited successfully!', 'user': user_serialized}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        