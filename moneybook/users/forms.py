from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "phone"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "아이디"
        self.fields["email"].label = "이메일"
        self.fields["phone"].label = "전화번호"
        self.fields["password1"].label = "비밀번호"
        self.fields["password2"].label = "비밀번호 확인"