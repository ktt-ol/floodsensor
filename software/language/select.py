def language(l):
    if l == "de_DE":
        import language.de_DE as lang
        
    print("Loaded "+ l +" locals file")