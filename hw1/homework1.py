### HOMEWORK1: MILLER_RABIN_PRIMALITY_TEST

from sympy import isprime
import random


#STEP1: DEFINIZIONE DELL'ALGORITMO

def miller_rabin_test(n,a): 
    q = n-1
    k = 0
    while q % 2 == 0:
        q //= 2
        k += 1
    x = pow(a, q, n) #calcola a^q mod n
    if x == 1:
        return True #se x è 1, allora n è probabilmente primo
    
    for j in range(k): 
        x = pow(x, 2 , n)  #calcola x^2 mod n (ovvero x^(2^j) mod n ricavata dai passaggi precedenti)
        if x == n-1:
            return True #se x è n-1, allora n è probabilmente primo
    
    return False #se x non è 1 o n-1, allora n è composto


#STEP2: TEST DELL'ALGORITMO CON SPECIFICHE HOMEWORK

def test_homework():

    primi = [n for n in range(10,1000) if isprime(n)]
    composti = [n for n in range(10,1000) if not isprime(n)]
    num_primi = random.sample(primi, 5) #seleziona 5 numeri primi casuali
    num_composti = random.sample(composti,5 ) #seleziona 5 numeri composti casuali
    
    print("\n\n*************************************")
    print("\n\nNumeri primi selezionati:  ", num_primi)
    print("\n\nNumeri composti selezionati:  ", num_composti)
    print("\n\n*************************************\n\nTest dei numeri selezionati:")
    
    for n in num_primi:
        a = random.randint(2, n-2) #base 'a' casuale tra 2 e n-2
        if miller_rabin_test(n, a):
            print(f"\n{n} è probabilmente primo (test con base {a}).")
        else:
            print(f"\n{n} è composto (test con base {a}).")

    for n in num_composti:
        a = random.randint(2, n-2) #base 'a' casuale tra 2 e n-2
        if miller_rabin_test(n, a):
            print(f"\n{n} è probabilmente primo (test con base {a}).")
        else:
            print(f"\n{n} è composto (test con base {a}).")

    print("\n *************************************")
    print("\n Test per n = 221 e a = 1, 21:\n")
    test_n = 221
    test_a = [1,21]
    for a in test_a:
        if miller_rabin_test(test_n, a):
            print(f"\n\n{test_n} è probabilmente primo (test con base {a}).")
        else:
            print(f"\n\n{test_n} è composto (test con base {a}).")
    print("\n *************************************")


#STEP3: TEST DELL'ALGORITMO CON INPUT DELL'UTENTE

def test_utente():

    print("\n\n**************************************\n\nTEST DELL'ALGORITMO DI MILLER-RABIN:\n\n**************************************\n\n")
    n = None
    a = None

    while True:
        scelta = input("\n\n Selezionare l'operazione da eseguire: \n1. Testare un numero\n2. Cambiare la base 'a'\n3. Testare specifiche homework \n4. Uscire\n")

        if scelta == '1':
            n = int(input("\n\nInserire il numero da testare: "))
            a = int(input("\nInserire la base 'a' con cui effettuare il test: "))
            if miller_rabin_test(n, a):
                print(f"\n{n} è probabilmente primo.\n ***************************************")
            else:
                print(f"\n{n} è composto. \n\n ***************************************")

        elif scelta == '2':
            if n is None:
                print("\nPrima di cambiare la base 'a', è necessario testare un numero.")
                continue

            a = int(input("\nInserire la nuova base 'a' con cui effettuare il test: "))
            if miller_rabin_test(n, a):
                print(f"\n{n} è probabilmente primo.\n ***************************************")
            else:
                print(f"\n{n} è composto.\n ***************************************")

        elif scelta == '3':
            test_homework()
        
        elif scelta == '4':
            print("\nUscita dal programma!")
            break

        else:
            print("\nScelta non valida. Riprova.")



test_utente()

    