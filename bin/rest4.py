def hey():
    try:
        print("Hellow")
        return "return my fun"
    except:
        print("exx")

    finally:
        print("Finallyy Donne")

h = hey()
print("Fun==>", h)