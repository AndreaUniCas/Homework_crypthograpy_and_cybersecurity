from operator import xor
import random


#PERMUTAZIONI
IP = [2,6,3,1,4,8,5,7]
IP_INV = [4,1,3,5,7,2,8,6]
P10 = [3,5,2,7,4,10,1,9,8,6]
P8 = [6,3,7,4,8,5,10,9]
P4 = [2,4,3,1]
EP = [4,1,2,3,2,3,4,1]

#S-BOXES
S0 = [[1,0,3,2],
      [3,2,1,0],
      [0,2,1,3],
      [3,1,3,2]]

S1 = [[0,1,2,3],
      [2,0,1,3],
      [3,0,1,0],
      [2,1,0,3]]

#FUNZIONI
def permutazione(msg, table):
    return [msg[i-1] for i in table]

def left_shift(msg, n):
    return msg[n:] + msg[:n]

def switch_halves(msg):
    mid = len(msg) // 2
    return msg[mid:] + msg[:mid]

def sbox_function(msg, sbox):
    row = (msg[0]*2 + msg[1]) 
    col = (msg[2]*2 + msg[3])
    val = sbox[row][col] 
    val_binary = [val // 2, val % 2] #conversione in binario(2 bit perchè in S-Box si va da 0 a 3)
    return val_binary

def generate_keys(key):
    key = permutazione(key, P10)
    key_left = left_shift(key[:5], 1)
    key_right = left_shift(key[5:], 1)
    key1 = permutazione(key_left + key_right, P8)
    key_left = left_shift(key_left, 2)
    key_right = left_shift(key_right, 2)
    key2 = permutazione(key_left + key_right, P8)
    return key1, key2

def F(msg_half2,key):
    msg_perm_ep = permutazione(msg_half2, EP) 
    msg_perm_ep_xor = [xor(msg_perm_ep[i], key[i]) for i in range(8)] #XOR tra msg_perm_ep e key
    msg_s0 = sbox_function(msg_perm_ep_xor[:4], S0)
    msg_s1 = sbox_function(msg_perm_ep_xor[4:], S1)
    msg_sbox = msg_s0 + msg_s1
    msg_perm_p4 = permutazione(msg_sbox, P4)
    return msg_perm_p4

def FunzioneK(msg, key):
    msg_left = msg[:4]
    msg_right = msg[4:]
    msg_F1 = F(msg_right, key)
    msg_xor1 = [xor(msg_left[i], msg_F1[i]) for i in range(len(msg_left))] #XOR tra msg_left e msg_F
    return msg_xor1 + msg_right

def encrypt(msg_plain,key1,key2):
    msg_ip = permutazione(msg_plain, IP)
    msg_crpt_in = FunzioneK(msg_ip, key1)
    switch_msg = switch_halves(msg_crpt_in)
    msg_crpt = FunzioneK(switch_msg, key2)
    msg_crpt = permutazione(msg_crpt, IP_INV)
    return msg_crpt

def decrypt(msg_cipher,key1,key2):
    msg_cipher_ip = permutazione(msg_cipher, IP)
    msg_decr_in = FunzioneK(msg_cipher_ip, key2)
    switch_msg = switch_halves(msg_decr_in) 
    msg_decr = FunzioneK(switch_msg, key1)
    msg_decr = permutazione(msg_decr, IP_INV)
    return msg_decr

#TEST
if __name__ == "__main__":
    key = random.choices(range(2), k=10) #Genera una chiave casuale di 10 bit
    print("Chiave generata:", ''.join(str(bit) for bit in key))
    key1, key2 = generate_keys(key)
    msg_utente = input("Inserire un messaggio di 8 bit (IN BINARIO): ")
    msg_encrypted = encrypt([int(bit) for bit in msg_utente], key1, key2)
    print("Messaggio cifrato:", ''.join(str(bit) for bit in msg_encrypted))
    msg_decrypted = decrypt(msg_encrypted, key1, key2)
    print("Messaggio decifrato:", ''.join(str(bit) for bit in msg_decrypted))



    


