from django.shortcuts import render

def dashboard(request):
    return render(request, 'dashboard.html')

def chat(request):
    temas = [
        "Construcción de paz",
        "Reconciliación",
        "Víctimas y memoria",
        "Juventud y paz",
        "Territorios de paz",
        "Comunicación no violenta",
    ]
    return render(request, 'chat.html', {"temas": temas})

def historias(request):
    return render(request, 'historias.html')
