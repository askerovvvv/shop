from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers
# from applications.account.send_mail import send_confirmation_email
from shop.tasks import send_confirmation_email

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(min_length=6, write_only=True, required=True)
    class Meta:
        model = User
        fields = ('email', 'password', 'password2')

    def validate(self, attrs): # в 'attrs' прилетает то что мы отослали(email, password, password2) VALIDATE - проверка
        password = attrs.get('password') # данные 1 пароля
        password2 = attrs.pop('password2') # удаляем 2 пароль и сохраняем в переменной

        if password != password2:
            raise serializers.ValidationError('Password do not match')
        return attrs # Если все хорошо нужно возвращать все данные

    # def validate_email(self, email):
    #     if not email.endswith('gmail.com'):
    #         raise serializers.ValidationError('your email must end with "gmail.com"" ')
    #     return email

    def create(self, validated_data): # логика регистрации
        user = User.objects.create_user(**validated_data) # принимает все данные которые прошли проверку
        code = user.activation_code  # наш активационный код передали новой переменной
        # send_confirmation_email(code, user) # импорт из send_mail.py | передаем в аргументы email и code


        send_confirmation_email.delay(code, user.email) # delay - указывает что он будет работать с celery
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)  # Работаем с емайл
    password = serializers.CharField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():     # filter это по типу WHERE в БД | exists = True or False
            raise serializers.ValidationError("Пользователь не найден")
        return email


    def validate(self, attrs):
        print('ffffffffffffffffffffffffffffffffffffffffffff1')
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password: # Если пароль и емайл существуют
            user = authenticate(username=email, password=password) # логин = емайл,  пароль = пароль -- для входа

            if not user:
                raise serializers.ValidationError("Неверный email или password")
            attrs['user'] = user # в attrs есть user он будет сохранен под новым user
            return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    password = serializers.CharField(required=True, min_length=6)
    password_confirm = serializers.CharField(required=True, min_length=6)

    def validate_old_password(self, old_pass):
        user = self.context.get('request').user  # Вытащили (текущего) User (с таким паролем)
        if not user.check_password(old_pass): # check_password = встроенный метод||| проверяет пароль USer
            raise serializers.ValidationError('Неверный пароль')
        return old_pass

    def validate(self, attrs):
        pass1 = attrs.get('password')
        pass2 = attrs.get('password_confirm')

        if pass1 != pass2:
            raise serializers.ValidationError('Пароль не совпадает')
        return attrs

    def set_user_password(self):
        user = self.context.get('request').user
        password = self.validated_data.get('password') #####
        user.set_password(password) # дали новый пароль и захешировали
        user.save()






# from django.contrib.auth import get_user_model, authenticate
# from rest_framework import serializers
#
# from applications.account.send_mail import send_confirmation_email
#
# User = get_user_model()
#
#
# class RegisterSerializer(serializers.ModelSerializer):
#     password2 = serializers.CharField(min_length=6, write_only=True, required=True)
#
#     class Meta:
#         model = User
#         fields = ('email', 'password', 'password2')
#
#     def validate(self, attrs):
#         password = attrs.get('password')
#         password2 = attrs.pop('password2')
#
#         if password != password2:
#             raise serializers.ValidationError('Password do not match!')
#         return attrs
#
#     def validate_email(self, email):
#         if not email.endswith("gmail.com"):
#             raise serializers.ValidationError("Your email must end with 'gmail.com'")
#         return email
#
#     def create(self, validated_data):
#         user = User.objects.create_user(**validated_data)
#         code = user.activation_code
#         send_confirmation_email(code, user)
#         return user
#
# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True)
#     password = serializers.CharField(required=True)
#
#     def validate_email(self, email):
#         if not User.objects.filter(email=email).exists():
#             raise serializers.ValidationError('Пользователь не зарегистрирован')
#         return email
#
#     def validate(self, attrs):
#         email = attrs.get('email')
#         password = attrs.get('password')
#
#         if email and password:
#             user = authenticate(username=email, password=password)
#             print(user)
#             if not user:
#                 raise serializers.ValidationError('Неверный email или password')
#             attrs['user'] = user
#             return attrs