import funzioni_hw3 as hw3

#FUNZIONI

def int_to_bin(n,bits):
    return [int(x) for x in bin(n)[2:].zfill(bits)]

def bin_to_int(bin_list):
    return int(''.join(str(x) for x in bin_list), 2)

#TEST
if __name__ == "__main__":

    #GENERAZIONE CHIAVI
    key1 = 123
    key2 = 1000
    key1_bin = int_to_bin(key1, 10)
    key2_bin = int_to_bin(key2, 10)
    keygen1,keygen2 = hw3.generate_keys(key1_bin)
    keygen3,keygen4 = hw3.generate_keys(key2_bin)
    print("Chiave 1 (decimale):", key1)
    print("Chiave 1 (binario):", ''.join(str(bit) for bit in key1_bin))
    print("Chiave 1 - Keygen 1 (binario):", ''.join(str(bit) for bit in keygen1))
    print("Chiave 1 - Keygen 2 (binario):", ''.join(str(bit) for bit in keygen2))
    print("Chiave 2 (decimale):", key2)
    print("Chiave 2 (binario):", ''.join(str(bit) for bit in key2_bin))
    print("Chiave 2 - Keygen 1 (binario):", ''.join(str(bit) for bit in keygen3))
    print("Chiave 2 - Keygen 2 (binario):", ''.join(str(bit) for bit in keygen4))

    #DOUBLE SDES
    plaintexts = [182, 124, 87]
    ciphertexts = []
    for pt in plaintexts:
        pt_bin = int_to_bin(pt, 8)
        print(f"Plaintext: {pt} (binario: {''.join(str(bit) for bit in pt_bin)})")
        cipher_intermedio = hw3.encrypt(pt_bin, keygen1,keygen2)
        cipher_finale = hw3.encrypt(cipher_intermedio, keygen3,keygen4)
        print(f"Cipher finale (binario): {''.join(str(bit) for bit in cipher_finale)}")
        cipher_finale_dec = bin_to_int(cipher_finale)
        ciphertexts.append(cipher_finale_dec)
    print("Ciphertexts finali (decimale):", ciphertexts)    
    
    #MEET IN THE MIDDLE ATTACK

    CHIAVI_POSSIBILI = range(1024)  # Tutte le chiavi possibili (10 bit)
    P1 = int_to_bin(plaintexts[0], 8)
    C1 = int_to_bin(ciphertexts[0], 8)
    tabella_encryption = {}
    tabella_decryption = {}
    key_candidate = []

    for key in CHIAVI_POSSIBILI:
        key_bin = int_to_bin(key, 10)
        k1, k2 = hw3.generate_keys(key_bin)
        X = hw3.encrypt(P1, k1, k2)
        key_X = tuple(X) #Convertiamo la lista in tupla per usarla come chiave nel dizionario
        if key_X not in tabella_encryption:
            tabella_encryption[key_X] = []
        tabella_encryption[key_X].append(key) #Memorizziamo tutte le chiavi che producono lo stesso X

    for key in CHIAVI_POSSIBILI:
        key_bin = int_to_bin(key, 10)
        k1, k2 = hw3.generate_keys(key_bin)
        Y = hw3.decrypt(C1, k1, k2)
        key_Y = tuple(Y)  #Convertiamo la lista in tupla per usarla come ch iave nel dizionario
        if key_Y not in tabella_decryption:
            tabella_decryption[key_Y] = []
        tabella_decryption[key_Y].append(key) #Memorizziamo tutte le chiavi che producono lo stesso Y

    for X in tabella_encryption:
        if X in tabella_decryption:
            for key_encryption in tabella_encryption[X]:
                for key_decryption in tabella_decryption[X]:
                    key_candidate.append((key_encryption, key_decryption))
    print("Chiavi candidate trovate:", len(key_candidate))

    # iteriamo sulle altre coppie P-C
    for i in range(1, len(plaintexts)):
        P = int_to_bin(plaintexts[i], 8)
        C = int_to_bin(ciphertexts[i], 8)
        new_key_candidate = []
        for key_encryption, key_decryption in key_candidate:
            k1_enc, k2_enc = hw3.generate_keys(int_to_bin(key_encryption, 10))
            k1_dec, k2_dec = hw3.generate_keys(int_to_bin(key_decryption, 10))
            X = hw3.encrypt(P, k1_enc, k2_enc)
            Y = hw3.decrypt(C, k1_dec, k2_dec)
            if X == Y:
                new_key_candidate.append((key_encryption, key_decryption))
        key_candidate = new_key_candidate
        print(f"Dopo la coppia P{i+1}-C{i+1}, chiavi candidate rimaste: {len(key_candidate)}")
    print("Chiavi candidate finali:", key_candidate)









    



