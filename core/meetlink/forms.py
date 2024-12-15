from django import forms


class LoginForm(forms.Form) :
    email = forms.EmailField(required=True, error_messages={
        "required": "O campo email é obrigatório.",
        "invalid": "Insira um email válido."
    })
    password = forms.CharField(widget=forms.PasswordInput, required=True, error_messages={
        "required": "O campo senha é obrigatório."
    })

class EditCallForm(forms.Form) :
    description = forms.CharField(max_length=500, required=False, error_messages={
        "max_length": "Máximo de 500 caracteres"
    })
    subject = forms.CharField(required=False)