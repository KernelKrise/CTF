idea: we have picture with pixels, and list of matching pixels gdb value and number. So i think we need to to read rgb values of pixels in picture and covert it to values and then to chars

to extract rgb values:

In [8]: from PIL import Image
   ...: 
   ...: im = Image.open('./intro_to_c.png', 'r')
   ...: 
   ...: pix_val = list(im.getdata())

In [9]: pix_val
Out[9]: 
[(182, 58, 13),
 (34, 174, 39),


read .txt file:



In [18]: res = dict()

In [19]: for i in text:
    ...:     o1 = 5
    ...:     o2 = i.find(', Val')
    ...:     o3 = i.find('RGB') + 3
    ...:     o4 = i.find(')') + 1
    ...:     key_val = i[o1:o2]
    ...:     rgb_val = i[o3:o4]
    ...:     res[rgb_val] = key_val

fg = list()

In [28]: for i in pix_val:
    ...:     fg.append(res[str(i)])
    ...:

In [35]: for i in fg:
    ...:     print(chr(int(i)), end='')
    ...: 
#include <stdio.h>

#define LEN(array) sizeof(array) / sizeof(*array)

#define SALT_1 97
#define SALT_2 4563246763
const long numbers[] = {4563246815, 4563246807, 4563246800, 4563246797, 4563246816, 4563246802, 4563246789, \
4563246780, 4563246783, 4563246850, 4563246843, 4563246771, 4563246765, 4563246825, 4563246781, 4563246784, \
4563246796, 4563246784, 4563246843, 4563246765, 4563246825, 4563246786, 4563246844, 4563246803, 4563246800, \
4563246825, 4563246775, 4563246852, 4563246843, 4563246778, 4563246825, 4563246781, 4563246849, 4563246782, \
4563246843, 4563246778, 4563246769, 4563246825, 4563246796, 4563246782, 4563246769, 4563246781, 4563246821, \
4563246823, 4563246827, 4563246827, 4563246827, 4563246791};

int main(void)
{
    size_t i;
    char undecyphered_char;

    for (i = 0; i < LEN(numbers); i++)
    {
        undecyphered_char = (char)((numbers[i] - SALT_2) ^ 97);

        printf("%c", undecyphered_char);
    }

    printf("\n");

    return 0;
}




┌──(kali㉿kali)-[~/Desktop/itc]
└─$ gcc solve.c -o solve
                                                                                                      
┌──(kali㉿kali)-[~/Desktop/itc]
└─$ chmod +x solve  
                                                                                                                    
┌──(kali㉿kali)-[~/Desktop/itc]
└─$ ./solve             
UMDCTF{pu61ic_st@t1c_v0ID_m81n_s7r1ng_@rgs[]!!!}
