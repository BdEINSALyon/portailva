from django import forms


class ExportForm(forms.Form):

    export_target = forms.ChoiceField(choices=(
        ('ALL', 'Toutes les associations'),
        ('LIVING', 'En activité'),
        ('DEAD', 'Mortes')
    ))

    export_data = forms.MultipleChoiceField(choices=(
        ('BASIC_DATA', 'Informations simples'),
        ('PRESIDENT_DATA', 'Coordonnées du président'),
        ('VALIDATIONS', 'Etats des validations')
    ))
