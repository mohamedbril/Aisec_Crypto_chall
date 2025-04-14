from Cryptodome.Util.number import *

def rot47(text):
    result = []
    for char in text:
        ascii_val = ord(char)
        if 33 <= ascii_val <= 126:  
            rotated = 33 + ((ascii_val - 33 + 47) % 94)
            result.append(chr(rotated))
        else:
            result.append(char)  
    return ''.join(result)


flag = "CRISIS{mr7ba_bik@baby_chall_rsa_o2KXl7VuByN5rQaTDzfp6cRM8gEwYv13nsqG9}"

flag_rot47 = rot47(flag)


n=0x00cd9ef3830d1c8b50909228ce38eb37a30a9f448cdeda805c086f489f2c8eed3543a72651f9403a1494afbcd03a95b703261ab399a98fcb7e9c84ce4ec28b863c51c8d0dba51899ea0adc32f2caf4c677902879c8f6eda7dc80f871e9cdfdfbeb7ebfa0b7c607b9fb5caedb8274ec65f1b89eae969d24566cd7e9f50d14b67ab9668374f41051f56730b0d1f883ac5bc240b461cf1e0272674552192618680690b549312c90136ad03341a0b4bf03073e9cfe5ead6583aef4e8dc525168b37bb9b2ed2da32b5f4d7f47dd516d262b80fbb520b31ef605883eddf7f49c8c1cfe964ce4759e61232184d5d80aace5589cbc33419d228e6e0fcd8416be4c77e62fff


e=0x10001

list_c =[]

for i in range(len(flag_rot47)):
    c = pow(bytes_to_long(flag_rot47[i].encode()), e, n)
    list_c.append(c)


with open("encrypted_values.txt", "w") as f:
    for i, c in enumerate(list_c, start=1):
        f.write(f"C{i} = {c}\n")
    f.close()