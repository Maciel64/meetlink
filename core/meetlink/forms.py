from django import forms


class LoginForm(forms.Form) :
    email = forms.EmailField(required=True, error_messages={
        "required": "O campo email é obrigatório.",
        "invalid": "Insira um email válido."
    })
    password = forms.CharField(widget=forms.PasswordInput, required=True, error_messages={
        "required": "O campo senha é obrigatório."
    })