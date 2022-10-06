// Decompiled with: CFR 0.152
// Class Version: 17
import java.util.Scanner;

public class Sekai {
    private static int length = (int)Math.pow(2.0, 3.0) - 2;

    public static void main(String[] stringArray) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter the flag: ");
        String string = scanner.next();
        if (string.length() != 43) {
            System.out.println("Oops, wrong flag!");
            return;
        }
        String string2 = string.substring(0, length);
        String string3 = string.substring(length, string.length() - 1);
        String string4 = string.substring(string.length() - 1);
        if (string2.equals("SEKAI{") && string4.equals("}")) {
            assert (string3.length() == length * length);
            if (Sekai.solve(string3)) {
                System.out.println("Congratulations, you got the flag!");
            } else {
                System.out.println("Oops, wrong flag!");
            }
        } else {
            System.out.println("Oops, wrong flag!");
        }
    }

    public static String encrypt(char[] cArray, int n) {
        int n2;
        char[] cArray2 = new char[length * 2];
        int n3 = length - 1;
        int n4 = length;
        for (n2 = 0; n2 < length * 2; ++n2) {
            cArray2[n2] = cArray[n3--];
            cArray2[n2 + 1] = cArray[n4++];
            ++n2;
        }
        n2 = 0;
        while (n2 < length * 2) {
            int n5 = n2++;
            cArray2[n5] = (char)(cArray2[n5] ^ (char)n);
        }
        return String.valueOf(cArray2);
    }

    public static char[] getArray(char[][] cArray, int n, int n2) {
        int n3;
        char[] cArray2 = new char[length * 2];
        int n4 = 0;
        for (n3 = 0; n3 < length; ++n3) {
            cArray2[n4] = cArray[n][n3];
            ++n4;
        }
        for (n3 = 0; n3 < length; ++n3) {
            cArray2[n4] = cArray[n2][length - 1 - n3];
            ++n4;
        }
        return cArray2;
    }

    public static char[][] transform(char[] cArray, int n) {
        char[][] cArray2 = new char[n][n];
        for (int i = 0; i < n * n; ++i) {
            cArray2[i / n][i % n] = cArray[i];
        }
        return cArray2;
    }

    public static boolean solve(String string) {
        char[][] cArray = Sekai.transform(string.toCharArray(), length);
        for (int i = 0; i <= length / 2; ++i) {
            for (int j = 0; j < length - 2 * i - 1; ++j) {
                char c = cArray[i][i + j];
                cArray[i][i + j] = cArray[length - 1 - i - j][i];
                cArray[Sekai.length - 1 - i - j][i] = cArray[length - 1 - i][length - 1 - i - j];
                cArray[Sekai.length - 1 - i][Sekai.length - 1 - i - j] = cArray[i + j][length - 1 - i];
                cArray[i + j][Sekai.length - 1 - i] = c;
            }
        }
        return "oz]{R]3l]]B#50es6O4tL23Etr3c10_F4TD2".equals(Sekai.encrypt(Sekai.getArray(cArray, 0, 5), 2) + Sekai.encrypt(Sekai.getArray(cArray, 1, 4), 1) + Sekai.encrypt(Sekai.getArray(cArray, 2, 3), 0));
    }
}
